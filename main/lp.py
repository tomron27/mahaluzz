import pandas as pd
import itertools
import pulp
import os
from mahaluzz.settings import BASE_DIR

def solve():

    # DRY Init
    DAYS = [1, 2, 3]
    HOURS = [1, 2, 3, 4, 5, 6]
    LESSONS = ['Math', 'Science']
    CLASSES = ['A1', 'A2']
    TEACHERS = ['Ruti', 'Shoshi']

    lessons_columns = ['Day', 'Hour', 'Lesson', 'Class', 'Teacher']
    lessons_data = pd.DataFrame(columns=lessons_columns)
    lessons_cart_input = (DAYS, HOURS, LESSONS, CLASSES, TEACHERS)

    teachers_const_columns = ['Teacher', 'Day', 'Hour', 'Value']
    teachers_data = pd.DataFrame(columns=teachers_const_columns)
    teachers_cart_input = (TEACHERS, DAYS, HOURS, [1])

    edu_const_columns = ['Class', 'Lesson', 'Value']
    edu_data = pd.DataFrame(columns=edu_const_columns)
    edu_cart_input = (CLASSES, LESSONS, [3])

    lessons_cart = itertools.product(*lessons_cart_input, repeat=1)
    teachers_cart = itertools.product(*teachers_cart_input, repeat=1)
    edu_cart = itertools.product(*edu_cart_input, repeat=1)

    print('expected num of variables: {}'.format(len(DAYS) * len(HOURS) * len(LESSONS) * len(CLASSES) * len(TEACHERS)))

    for i, out in enumerate(lessons_cart):
        lessons_data.loc[i] = out
    print(lessons_data.shape)

    for i, out in enumerate(teachers_cart):
        teachers_data.loc[i] = out
    teachers_data = teachers_data.drop_duplicates()
    print(teachers_data.shape)

    for i, out in enumerate(edu_cart):
        edu_data.loc[i] = out
    edu_data = edu_data.drop_duplicates()
    print(edu_data.shape)

    dummy_data =  {'Teacher': ['Ruti', 'Ruti', 'Shoshi', 'Shoshi'],
                   'Lesson': ['Math', 'Science', 'Math', 'Science'],
                   'Value': [1, 1, 0, 1]}

    teachers_lesson_data = pd.DataFrame(data=dummy_data)

    print(teachers_lesson_data.shape)

    lessons_dict = pulp.LpVariable.dicts("variables",
                                         ((row.Day, row.Hour, row.Lesson, row.Class, row.Teacher) for row in
                                          lessons_data.itertuples()),
                                         lowBound=0,
                                         cat='Binary')

    all_data = lessons_data.merge(teachers_data, on=['Teacher', 'Day', 'Hour'])
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
    #     print(expr, '\n\n')
        model += expr

    model.solve()

    return pulp.LpStatus[model.status], lessons_dict
