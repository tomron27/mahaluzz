import pandas as pd
import itertools
import pulp
from main.models import *
import os

class Model:

    def get_teachers_with_subjects(self):
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

    def get_teachers(self):
        query_list = Classroom.objects.all().values_list()
        return list(set([x[2] for x in query_list]))

    def get_lessons(self):
        query_list = Tsubject.objects.all().values_list()
        return list(set([x[2] for x in query_list]))

    def get_classes(self):
        query_list = Classroom.objects.all().values_list()
        return list(set([x[1] for x in query_list]))

    def get_education_constratints(self):
        teachers_with_subjects = pd.DataFrame.from_records(Tsubject.objects.all().values())
        subjects_with_quants = pd.DataFrame.from_records(Aconstraint.objects.all().values())
        teachers_with_classrooms = pd.DataFrame.from_records(Classroom.objects.all().values())

        all = teachers_with_subjects.merge(subjects_with_quants, on=['subject']).merge(teachers_with_classrooms, on=['teacher'])

        all = all[['name', 'subject', 'h_quantity']]\
            .drop_duplicates()\
            .rename(columns={'name': 'Class', 'subject': 'Lesson', 'h_quantity': 'Value'})

        return all

    def get_teacher_constraints(self):
        teacher_constraints = pd.DataFrame.from_records(Tconstraint.objects.all().values())
        teacher_constraints = teacher_constraints[['teacher', 'day_of_week', 'hour', 'priority']]
        teacher_constraints = teacher_constraints.rename(columns={'teacher': 'Teacher', 'day_of_week': 'Day', 'hour': 'Hour', 'priority': 'Value'})\
            .drop_duplicates()

        return teacher_constraints



    def solve(self):

        # META DATA
        self.DAYS = [1, 2, 3, 4, 5, 6]
        self.HOURS = [1, 2, 3, 4, 5, 6, 7]
        self.LESSONS = self.get_lessons()
        self.CLASSES = self.get_classes()
        self.TEACHERS = self.get_teachers()

        # Teacher constraints data
        teachers_data = self.get_teacher_constraints()

        # Dep. of education constraints
        edu_data = self.get_education_constratints()

        # Teachers that teach certain lessons
        teachers_lesson_data = self.get_teachers_with_subjects()

        # Main basis for variables
        lessons_cart = itertools.product(self.DAYS, self.HOURS, self.LESSONS, self.CLASSES, self.TEACHERS, repeat=1)
        # lessons_data = pd.DataFrame.from_records(lessons_cart, columns=['Day', 'Hour', 'Lesson', 'Class', 'Teacher'])
        lessons_data = pd.DataFrame(columns=['Day', 'Hour', 'Lesson', 'Class', 'Teacher'])

        j = 0
        for row in lessons_cart:
            if '_' not in row[2] or row[3] in row[2]: # subject is like "sport" or subject matches the class (a1 <=> math_a1)
                lessons_data.loc[j] = row
                j += 1
                # horrible coding

        lessons_data = lessons_data.infer_objects()

        print('expected num of variables: {}'.format(len(self.DAYS) * len(self.HOURS) * len(self.LESSONS) * len(self.CLASSES) * len(self.TEACHERS)))

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

        print('all_data')
        print(all_data.head(4))
        print(all_data.shape)

        model = pulp.LpProblem("Schedule LP Problem - minimize amount of windows", pulp.LpMinimize)

        # Objective function build

        # For each class, day, teacher - give high penalty for late scheduling.
        expr = []
        for row in lessons_data[['Day', 'Class', 'Teacher']].drop_duplicates().itertuples():
            sub_expr = []
            for sub_row in lessons_data[(lessons_data['Day'] == row.Day) &
                                        (lessons_data['Class'] == row.Class) &
                                        (lessons_data['Teacher'] == row.Teacher)].drop_duplicates().itertuples():
                if row.Day == 6:    # Penalize friday
                    sub_expr += lessons_dict[
                                    row.Day, sub_row.Hour, sub_row.Lesson, row.Class, row.Teacher] * sub_row.Hour * 2
                else:
                    sub_expr += lessons_dict[
                                    row.Day, sub_row.Hour, sub_row.Lesson, row.Class, row.Teacher] * sub_row.Hour
            expr += sub_expr
        model += pulp.lpSum(expr)

        # Constraints

        # Force break on 4th period
        lp_sum = []
        for row in lessons_data[lessons_data['Hour'] == 4].drop_duplicates().itertuples():
            lp_sum += lessons_dict[row.Day, row.Hour, row.Lesson, row.Class, row.Teacher]
        expr = (lp_sum == 0)
        model += expr

        # How many hours for every class for every lesson
        for edu_row in edu_data.itertuples():
            lp_sum = []
            for lesson_row in lessons_data[(lessons_data['Lesson'] == edu_row.Lesson) & (
                    lessons_data['Class'] == edu_row.Class)].drop_duplicates().itertuples():
                lp_sum += lessons_dict[
                    lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
            expr = (lp_sum == edu_row.Value)
            model += expr

        # Teachers can teach only one class per hour
        for row in lessons_data[['Teacher', 'Day', 'Hour']].drop_duplicates().itertuples():
            lp_sum = []
            for lesson_row in lessons_data[(lessons_data['Teacher'] == row.Teacher) &
                                           (lessons_data['Day'] == row.Day) & (lessons_data['Hour'] == row.Hour)].drop_duplicates().itertuples():
                lp_sum += lessons_dict[lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
            expr = (lp_sum <= 1)
        #     print(expr, '\n\n')
            model += expr

        # Classes can have only one lesson per hour
        for row in lessons_data[['Class', 'Day', 'Hour']].drop_duplicates().itertuples():
            lp_sum = []
            for lesson_row in lessons_data[(lessons_data['Class'] == row.Class) & (lessons_data['Day'] == row.Day) & (
                    lessons_data['Hour'] == row.Hour)].drop_duplicates().itertuples():
                lp_sum += lessons_dict[
                    lesson_row.Day, lesson_row.Hour, lesson_row.Lesson, lesson_row.Class, lesson_row.Teacher]
            expr = (lp_sum <= 1)
            #     print(expr, '\n\n')
            model += expr

        # Teacher lessons constraints
        for row in lessons_data.drop_duplicates().itertuples():
            expr = (lessons_dict[row.Day, row.Hour, row.Lesson, row.Class, row.Teacher] <=
                    teachers_lesson_data[(teachers_lesson_data['Teacher'] == row.Teacher) &
                                         (teachers_lesson_data['Lesson'] == row.Lesson)]['Value'])
            model += expr

        print('Printing model...')
        with open('model.txt', 'w', encoding="utf-8") as f:
            print('Datetime:', datetime.datetime.now)
            print(model, file=f)

        model.solve()

        lessons_output = []
        for k, v in lessons_dict.items():
            if v.varValue == 1:
                lessons_output.append(k)

        print('Model status:', pulp.LpStatus[model.status])
        print('Solution:')
        print(lessons_output)

        return pulp.LpStatus[model.status], lessons_output
