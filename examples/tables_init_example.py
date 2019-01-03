# from schedule.models import *
# import datetime
#
# start_hour = 8
# start_minute = 0
# day = 9
# month = 12
# year = 2018
#
#
# def save(objects, table=None):
#     if table is not None:
#         table.objects.all().delete()
#     for obj in objects:
#         obj.save()
#
#
# classrooms = [Classroom(name="חדר כיתה א1", capacity=40), Classroom(name="חדר כיתה א2", capacity=40),
#               Classroom(name="חדר כיתה א3", capacity=40)]
#
# lessons = [
#     Lesson(start_time=datetime.datetime(year, month, day, start_hour, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day, start_hour + 1, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day, start_hour + 3, start_minute), title="מדעים", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day, start_hour + 4, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#
#     Lesson(start_time=datetime.datetime(year, month, day + 1, start_hour, start_minute), title="תנ\"ך", _class="א1",
#            location="חדר כיתה א1", has_hw=True),
#     Lesson(start_time=datetime.datetime(year, month, day + 1, start_hour + 1, start_minute), title="תנ\"ך", _class="א1",
#            location="חדר כיתה א1", has_hw=True),
#     Lesson(start_time=datetime.datetime(year, month, day + 1, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day + 1, start_hour + 3, start_minute), title="עברית", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 1, start_hour + 4, start_minute), title="ספורט", _class="א1",
#            location="חצר א'-ב'"),
#
#     Lesson(start_time=datetime.datetime(year, month, day + 2, start_hour, start_minute), title="אמנות", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 2, start_hour + 1, start_minute), title="אמנות", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 2, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day + 2, start_hour + 3, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 2, start_hour + 4, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#
#     Lesson(start_time=datetime.datetime(year, month, day + 3, start_hour, start_minute), title="מדעים", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 3, start_hour + 1, start_minute), title="מדעים", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 3, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day + 3, start_hour + 3, start_minute), title="מוזיקה", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 3, start_hour + 4, start_minute), title="ספורט", _class="א1",
#            location="חצר א'-ב'"),
#
#     Lesson(start_time=datetime.datetime(year, month, day + 4, start_hour, start_minute), title="חשבון", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 4, start_hour + 1, start_minute), title="מוזיקה", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 4, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day + 4, start_hour + 3, start_minute), title="עברית", _class="א1",
#            location="חדר כיתה א1", has_hw=True),
#     Lesson(start_time=datetime.datetime(year, month, day + 4, start_hour + 4, start_minute), title="עברית", _class="א1",
#            location="חדר כיתה א1", has_hw=True),
#
#     Lesson(start_time=datetime.datetime(year, month, day + 5, start_hour, start_minute), title="חינוך", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 5, start_hour + 1, start_minute), title="עברית", _class="א1",
#            location="חדר כיתה א1"),
#     Lesson(start_time=datetime.datetime(year, month, day + 5, start_hour + 2, start_minute), title="הפסקה", _class="א1",
#            location="חצר א'-ב'"),
#     Lesson(start_time=datetime.datetime(year, month, day + 5, start_hour + 3, start_minute), title="חינוך", _class="א1",
#            location="חדר כיתה א1"),
# ]
#
# save(classrooms, Classroom)
# save(lessons, Lesson)
