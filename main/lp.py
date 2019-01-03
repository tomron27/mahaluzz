import pandas as pd
import itertools
import pulp
from main.models import *
import os
from mahaluzz.settings import BASE_DIR

def get_teachers_with_subjects():
    query_list = Tsubject.objects.all().values_list()
    teachers = list(set([x[1] for x in query_list]))
    subjects = list(set([x[2] for x in query_list]))
    teachers_with_subjects = set([(x[1], x[2]) for x in query_list])
    cartesian = itertools.product(teachers, subjects, repeat=1)
    teachers_lesson_data = pd.DataFrame(columns=['Teacher', 'Lesson', 'Value'])
    for i, teacher_subject in enumerate(cartesian):
        if teacher_subject in teachers_with_subjects:
            teachers_lesson_data.loc[i] = (teacher_subject[0], teacher_subject[1], 1)
        else:
            teachers_lesson_data.loc[i] = (teacher_subject[0], teacher_subject[1], 0)
    return teachers_lesson_data

def get_teachers():
    query_list = Classroom.objects.all().values_list()
    return list(set([x[1] for x in query_list]))

def get_lessons():
    query_list = Tsubject.objects.all().values_list()
    return list(set([x[2] for x in query_list]))

def get_classes():
    query_list = Classroom.objects.all().values_list()
    return list(set([x[0] for x in query_list]))

def get_education_constratints():
    teachers_with_subjects = pd.DataFrame.from_records(Tsubject.objects.all().values())
    subjects_with_quants = pd.DataFrame.from_records(Aconstraint.objects.all().values())
    teachers_with_classrooms = pd.DataFrame.from_records(Classroom.objects.all().values())

    all = teachers_with_subjects.merge(subjects_with_quants, on=['subject'])\
        .merge(teachers_with_classrooms, on=['teacher'])

    all = all[['name', 'subject', 'h_quantity']]\
        .drop_duplicates()\
        .rename(columns={'name': 'Class', 'subject': 'Lesson', 'h_quantity': 'Value'})

    return all

def get_teacher_constraints():
    teacher_constraints = pd.DataFrame.from_records(Tconstraint.objects.all().values())
    teacher_constraints = teacher_constraints[['teacher', 'day_of_week', 'hour', 'priority']]
    teacher_constraints = teacher_constraints.rename(columns={'teacher': 'Teacher', 'day_of_week': 'Day', 'hour': 'Hour', 'priority': 'Value'})\
        .drop_duplicates()

    return teacher_constraints

def solve():

    # DRY Init
    DAYS = [1, 2, 3, 4, 5, 6]
    HOURS = [1, 2, 3, 4, 5, 6]
    LESSONS = get_lessons()
    CLASSES = get_classes()
    TEACHERS = get_teachers()

    # Teacher constraints data
    teachers_data = get_teacher_constraints()

    # Dep. of education constraints
    edu_data = get_education_constratints()

    # Teachers that teach certain lessons
    teachers_lesson_data = get_teachers_with_subjects()

    # Main basis for variables
    lessons_cart = itertools.product(DAYS, HOURS, LESSONS, CLASSES, TEACHERS, repeat=1)
    # lessons_data = pd.DataFrame.from_records(lessons_cart, columns=['Day', 'Hour', 'Lesson', 'Class', 'Teacher'])
    lessons_data = pd.DataFrame(columns=['Day', 'Hour', 'Lesson', 'Class', 'Teacher'])

    j = 0
    for row in lessons_cart:
        if '_' not in row[2] or row[3] in row[2]: # subject is like "sport" or subject matches the class (a1 <=> math_a1)
            lessons_data.loc[j] = row
            j += 1
            # horrible coding

    lessons_data = lessons_data.infer_objects()

    print('expected num of variables: {}'.format(len(DAYS) * len(HOURS) * len(LESSONS) * len(CLASSES) * len(TEACHERS)))

    print('teachers_data')
    print(teachers_data.head(4))
    print(teachers_data.shape)

    print('edu_data')
    print(edu_data.head(4))
    print(edu_data.shape)

    print('teachers_lesson_data')
    print(teachers_lesson_data.head(4))
    print(teachers_lesson_data.shape)

    print('lessons_data')
    print(lessons_data.head(4))
    print(lessons_data.shape)

    lessons_dict = pulp.LpVariable.dicts("variables",
                                         ((row.Day, row.Hour, row.Lesson, row.Class, row.Teacher) for row in
                                          lessons_data.itertuples()),
                                         lowBound=0,
                                         cat='Binary')

    all_data = lessons_data.merge(teachers_data, on=['Teacher', 'Day', 'Hour'])

    print(all_data.head(4))

    model = pulp.LpProblem("Minimize amount of lessons", pulp.LpMinimize)

    # Objective function build
    expr = []
    for row in all_data.itertuples():
        expr += lessons_dict[row.Day, row.Hour, row.Lesson, row.Class, row.Teacher] * row.Value
    model += expr

    # How many hours for every class for every lesson
    for edu_row in edu_data.itertuples():
        lp_sum = []
        expr = pulp.LpAffineExpression()
        for lesson_row in lessons_data[(lessons_data['Lesson'] == edu_row.Lesson) & (
                lessons_data['Class'] == edu_row.Class)].drop_duplicates().itertuples():
            lp_sum += lessons_dict[
                lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
        expr = (lp_sum == edu_row.Value)
        model += expr

    # Teachers can teach only one class per hour
    for row in lessons_data[['Teacher', 'Day', 'Hour']].drop_duplicates().itertuples():
        lp_sum = []
        expr = pulp.LpAffineExpression()
        for lesson_row in lessons_data[(lessons_data['Teacher'] == row.Teacher) &
                                       (lessons_data['Day'] == row.Day) & (lessons_data['Hour'] == row.Hour)].drop_duplicates().itertuples():
            lp_sum += lessons_dict[lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
        expr = (lp_sum <= 1)
    #     print(expr, '\n\n')
        model += expr

    # Classes can have only one lesson per hour
    for row in lessons_data[['Class', 'Day', 'Hour']].drop_duplicates().itertuples():
        lp_sum = []
        expr = pulp.LpAffineExpression()
        for lesson_row in lessons_data[(lessons_data['Class'] == row.Class) & (lessons_data['Day'] == row.Day) & (
                lessons_data['Hour'] == row.Hour)].drop_duplicates().itertuples():
            lp_sum += lessons_dict[
                lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
        expr = (lp_sum <= 1)
        #     print(expr, '\n\n')
        model += expr

    # Window variables
    L_dict = pulp.LpVariable.dicts("variables",
                                   ((row.Day, row.Hour, row.Class, 'L') for row in
                                    lessons_data[['Day', 'Hour', 'Class']].drop_duplicates().itertuples()),
                                   lowBound=0,
                                   cat='Binary')

    Y_dict = pulp.LpVariable.dicts("variables",
                                   ((row.Day, row.Hour, row.Class, 'Y') for row in
                                    lessons_data[['Day', 'Hour', 'Class']].drop_duplicates().itertuples()),
                                   lowBound=0,
                                   cat='Binary')

    Z_dict = pulp.LpVariable.dicts("variables",
                                   ((row.Day, row.Hour, row.Class, 'Z') for row in
                                    lessons_data[['Day', 'Hour', 'Class']].drop_duplicates().itertuples()),
                                   lowBound=0,
                                   cat='Binary')

    # Window constraints
    for row, L_ijl in L_dict.items():
        expr = pulp.LpAffineExpression()
        sub_expr = pulp.LpAffineExpression()
        lp_sum = []
        for sub_row in lessons_data[(lessons_data['Day'] == row[0]) & (lessons_data['Hour'] == row[1]) & (
                lessons_data['Class'] == row[2])].drop_duplicates().itertuples():
            lp_sum += lessons_dict[sub_row.Day, sub_row.Hour, sub_row.Lesson, sub_row.Class, sub_row.Teacher]
        expr = (L_ijl - lp_sum == 0)
        #     print(expr)
        model += expr

    for row, L_ijl in L_dict.items():
        if row[1] <= max(HOURS) - 1:
            expr = pulp.LpAffineExpression()
            expr = (L_dict[row] - L_dict[(row[0], row[1] + 1, row[2], 'L')] + Y_dict[
                (row[0], row[1] + 1, row[2], 'Y')] - Z_dict[(row[0], row[1] + 1, row[2], 'Z')] == 0)
            model += expr

    for row in lessons_data[['Class', 'Day', 'Hour']].drop_duplicates().itertuples():
        lp_sum = []
        expr = pulp.LpAffineExpression()
        for lesson_row in lessons_data[['Class', 'Day', 'Hour']][
            (lessons_data['Class'] == row.Class) & (lessons_data['Day'] == row.Day)].drop_duplicates().itertuples():
            lp_sum += Y_dict[lesson_row.Day, lesson_row.Hour, lesson_row.Class, 'Y']
        expr = (lp_sum <= 1)
        #     print(expr, '\n\n')
        model += expr

    for row in lessons_data[['Class', 'Day', 'Hour']].drop_duplicates().itertuples():
        lp_sum = []
        expr = pulp.LpAffineExpression()
        for lesson_row in lessons_data[['Class', 'Day', 'Hour']][
            (lessons_data['Class'] == row.Class) & (lessons_data['Day'] == row.Day)].drop_duplicates().itertuples():
            lp_sum += Z_dict[lesson_row.Day, lesson_row.Hour, lesson_row.Class, 'Z']
        expr = (lp_sum <= 1)
        #     print(expr, '\n\n')
        model += expr

    # Teacher lessons constraints
    for row in lessons_data.drop_duplicates().itertuples():
        expr = pulp.LpAffineExpression()
        expr = (lessons_dict[row.Day, row.Hour, row.Lesson, row.Class, row.Teacher] <=
                teachers_lesson_data[(teachers_lesson_data['Teacher'] == row.Teacher) &
                                     (teachers_lesson_data['Lesson'] == row.Lesson)]['Value'])
        model += expr

    model.solve()



    lessons_output = []
    for k, v in lessons_dict.items():
        if v.varValue == 1:
            lessons_output.append(k)

    print('Model status:', pulp.LpStatus[model.status])
    print('Solution:')
    print(lessons_output)

    return pulp.LpStatus[model.status], lessons_output
