import pandas as pd
import itertools
import pulp

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

    teachers_lesson_data = pd.read_csv('teacher_lessons.csv')
    print(teachers_lesson_data.shape)