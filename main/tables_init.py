from main.models import *


def save(objects, table=None):
    if table is not None:
        table.objects.all().delete()
    for obj in objects:
        obj.save()


Classrooms = [Classroom(name="א1", teacher="ruti"), Classroom(name="ג1", teacher="shush")]

Students = [Student(id="302077633", first_name="שיר", last_name="כהן", parent1="haimcohen", parent2="dorit", classroom="א1", birthday='2003-01-17'),
            Student(id="302077634", first_name="דורון", last_name="כהן", parent1="haimcohen", parent2="dorit", classroom="ג1", birthday='2005-01-20'),
            Student(id="302077635", first_name="תום", last_name="כהן", parent1="haimcohen", parent2="dorit", classroom="ג1", birthday='2005-01-20'),
            Student(id="302077636", first_name="נעמי", last_name="טננבאום",parent1="shaolm", parent2="noga", classroom="א1", birthday='2003-04-20')]

Events = [Event(name='טקס ט"ו בשבת', day=14, month=1, hour=8)]

Tsubjects = [Tsubject(t_sub_id=1, teacher="ruti", subject="חשבון_א1"),
             Tsubject(t_sub_id=2, teacher="ruti", subject="שפה_א1"),
             Tsubject(t_sub_id=3, teacher="ruti", subject="מדעים_א1"),
             Tsubject(t_sub_id=4, teacher="ruti", subject="חינוך_א1"),
             Tsubject(t_sub_id=4, teacher="ruti", subject="הנדסה_א1"),
             Tsubject(t_sub_id=5, teacher="shush", subject="חשבון_ג1"),
             Tsubject(t_sub_id=6, teacher="shush", subject="תנך_ג1"),
             Tsubject(t_sub_id=7, teacher="shush", subject="מדעים_ג1"),
             Tsubject(t_sub_id=8, teacher="shush", subject="עברית_ג1"),
             Tsubject(t_sub_id=9, teacher="shush", subject="חינוך_ג1"),
             Tsubject(t_sub_id=10, teacher="shush", subject="הנדסה_ג1"),
             Tsubject(t_sub_id=11, teacher="shush", subject="גיאוגרפיה_ג1"),
             Tsubject(t_sub_id=12, teacher="bar", subject="אנגלית"),
             Tsubject(t_sub_id=13, teacher="nurit", subject="ספורט"),
             Tsubject(t_sub_id=14, teacher="hila", subject="אומנות")]

Schedules = [Schedule(schedule_id=1, day_of_week=1, hour=1, classroom='א1', teacher='ruti', subject='חשבון'),
             Schedule(schedule_id=2, day_of_week=1, hour=2, classroom='א1', teacher='ruti', subject='חשבון'),
             Schedule(schedule_id=3, day_of_week=1, hour=3, classroom='א1', teacher='ruti', subject='מדעים'),
             Schedule(schedule_id=4, day_of_week=1, hour=4, classroom='א1', teacher='ruti', subject='מדעים'),
             Schedule(schedule_id=5, day_of_week=1, hour=5, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=6, day_of_week=1, hour=6, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=7, day_of_week=2, hour=1, classroom='א1', teacher='ruti', subject='חשבון'),
             Schedule(schedule_id=8, day_of_week=2, hour=2, classroom='א1', teacher='ruti', subject='חשבון'),
             Schedule(schedule_id=9, day_of_week=2, hour=3, classroom='א1', teacher='ruti', subject='ספרות'),
             Schedule(schedule_id=10, day_of_week=2, hour=4, classroom='א1', teacher='ruti', subject='ספרות'),
             Schedule(schedule_id=11, day_of_week=2, hour=5, classroom='א1', teacher='ruti', subject='טוורקינג'),
             Schedule(schedule_id=12, day_of_week=2, hour=6, classroom='א1', teacher='ruti', subject='טוורקינג'),
             Schedule(schedule_id=13, day_of_week=3, hour=1, classroom='א1', teacher='ruti', subject='סטוכסטים'),
             Schedule(schedule_id=14, day_of_week=3, hour=2, classroom='א1', teacher='ruti', subject='סטוכסטים'),
             Schedule(schedule_id=15, day_of_week=3, hour=3, classroom='א1', teacher='ruti', subject='מד"ר'),
             Schedule(schedule_id=16, day_of_week=3, hour=4, classroom='א1', teacher='ruti', subject='מד"ר'),
             Schedule(schedule_id=17, day_of_week=3, hour=5, classroom='א1', teacher='ruti', subject='אינפי 3'),
             Schedule(schedule_id=18, day_of_week=3, hour=6, classroom='א1', teacher='ruti', subject='אינפי 3'),
             Schedule(schedule_id=19, day_of_week=4, hour=1, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=20, day_of_week=4, hour=2, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=21, day_of_week=4, hour=3, classroom='א1', teacher='ruti', subject='האדם וחיות הבית'),
             Schedule(schedule_id=22, day_of_week=4, hour=4, classroom='א1', teacher='ruti', subject='האדם וחיות הבית'),
             Schedule(schedule_id=23, day_of_week=4, hour=5, classroom='א1', teacher='ruti', subject='באולינג'),
             Schedule(schedule_id=24, day_of_week=4, hour=6, classroom='א1', teacher='ruti', subject='באולינג'),
             Schedule(schedule_id=25, day_of_week=5, hour=1, classroom='א1', teacher='ruti', subject='אנערף'),
             Schedule(schedule_id=26, day_of_week=5, hour=2, classroom='א1', teacher='ruti', subject='אנערף'),
             Schedule(schedule_id=27, day_of_week=5, hour=3, classroom='א1', teacher='ruti', subject='אנערף'),
             Schedule(schedule_id=28, day_of_week=5, hour=4, classroom='א1', teacher='ruti', subject='אנערף'),
             Schedule(schedule_id=29, day_of_week=5, hour=5, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=30, day_of_week=5, hour=6, classroom='א1', teacher='ruti', subject='תנ"ך'),
             Schedule(schedule_id=31, day_of_week=6, hour=1, classroom='א1', teacher='ruti', subject='ריקוד על עמוד'),
             Schedule(schedule_id=32, day_of_week=6, hour=2, classroom='א1', teacher='ruti', subject='ריקוד על עמוד'),
             Schedule(schedule_id=33, day_of_week=6, hour=3, classroom='א1', teacher='ruti', subject='מבוא להעלמת מס'),
             Schedule(schedule_id=34, day_of_week=6, hour=4, classroom='א1', teacher='ruti', subject='מבוא להעלמת מס'),
             Schedule(schedule_id=35, day_of_week=6, hour=5, classroom='א1', teacher='ruti', subject='מטעני חבלה 2'),
             Schedule(schedule_id=36, day_of_week=6, hour=6, classroom='א1', teacher='ruti', subject='מטעני חבלה 2')]

save(Classrooms)
save(Students)
save(Events)
save(Tsubjects)
save(Schedules)
