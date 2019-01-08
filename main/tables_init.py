from main.models import *


def save(objects, table=None):
    if table is not None:
        table.objects.all().delete()
    for obj in objects:
        obj.save()


Classrooms = [Classroom(class_id=0, name="א1", teacher="ruti"), Classroom(class_id=1, name="ג1", teacher="shush"),
              Classroom(class_id=2, name="ב2", teacher="hadar"), Classroom(class_id=15, name="ד2", teacher="shlomit"),
              Classroom(class_id=3, name="א1", teacher="nurit"), Classroom(class_id=4, name="ג1", teacher="nurit"),
              Classroom(class_id=5, name="ב2", teacher="nurit"), Classroom(class_id=6, name="ד2", teacher="nurit"),
              Classroom(class_id=7, name="א1", teacher="eti"), Classroom(class_id=8, name="ג1", teacher="eti"),
              Classroom(class_id=9, name="ב2", teacher="eti"), Classroom(class_id=10, name="ד2", teacher="eti"),
              Classroom(class_id=11, name="א1", teacher="hila"), Classroom(class_id=12, name="ג1", teacher="hila"),
              Classroom(class_id=13, name="ב2", teacher="hila"), Classroom(class_id=14, name="ד2", teacher="hila"), ]

Students = [Student(id="302077633", first_name="שיר", last_name="כהן", parent1="haimcohen", parent2="dorit",
            classroom="א1", birthday='2013-01-17'), Student(id="302077634", first_name="דורון",
            last_name="כהן", parent1="haimcohen", parent2="dorit", classroom="ג1", birthday='2011-01-20'),
            Student(id="302077635", first_name="תום", last_name="כהן", parent1="haimcohen", parent2="dorit",
            classroom="ב2", birthday='2012-01-20'), Student(id="302077636", first_name="נעמי",
            last_name="טננבאום", parent1="shaolm", parent2="noga", classroom="ד2", birthday='2010-04-20')]

Events = [Event(name='טקס ט"ו בשבת', day=14, month=1, hour=8)]

Tsubjects = [Tsubject(t_sub_id=1, teacher="ruti", subject="חשבון_א1"),
             Tsubject(t_sub_id=30, teacher="ruti", subject="תורה_א1"),
             Tsubject(t_sub_id=2, teacher="ruti", subject="שפה_א1"),
             Tsubject(t_sub_id=3, teacher="ruti", subject="מדעים_א1"),
             Tsubject(t_sub_id=4, teacher="ruti", subject="חינוך_א1"),
             Tsubject(t_sub_id=15, teacher="ruti", subject="הנדסה_א1"),
             Tsubject(t_sub_id=5, teacher="shush", subject="חשבון_ג1"),
             Tsubject(t_sub_id=6, teacher="shush", subject="תנך_ג1"),
             Tsubject(t_sub_id=7, teacher="shush", subject="מדעים_ג1"),
             Tsubject(t_sub_id=8, teacher="shush", subject="עברית_ג1"),
             Tsubject(t_sub_id=9, teacher="shush", subject="חינוך_ג1"),
             Tsubject(t_sub_id=10, teacher="shush", subject="הנדסה_ג1"),
             Tsubject(t_sub_id=11, teacher="shush", subject="גיאוגרפיה_ג1"),
             Tsubject(t_sub_id=31, teacher="shlomit", subject="חשבון_ד2"),
             Tsubject(t_sub_id=18, teacher="shlomit", subject="תנך_ד2"),
             Tsubject(t_sub_id=19, teacher="shlomit", subject="מדעים_ד2"),
             Tsubject(t_sub_id=20, teacher="shlomit", subject="עברית_ד2"),
             Tsubject(t_sub_id=21, teacher="shlomit", subject="חינוך_ד2"),
             Tsubject(t_sub_id=22, teacher="shlomit", subject="הנדסה_ד2"),
             Tsubject(t_sub_id=23, teacher="shlomit", subject="גיאוגרפיה_ד2"),
             Tsubject(t_sub_id=12, teacher="bar", subject="אנגלית_ג1"),
             Tsubject(t_sub_id=13, teacher="nurit", subject="ספורט"),
             Tsubject(t_sub_id=16, teacher="eti", subject="מוזיקה"),
             Tsubject(t_sub_id=14, teacher="hila", subject="אומנות"),
             Tsubject(t_sub_id=17, teacher="bar", subject="אנגלית_ד2"),
             Tsubject(t_sub_id=24, teacher="hadar", subject="חשבון_ב2"),
             Tsubject(t_sub_id=25, teacher="hadar", subject="תורה_ב2"),
             Tsubject(t_sub_id=26, teacher="hadar", subject="שפה_ב2"),
             Tsubject(t_sub_id=27, teacher="hadar", subject="מדעים_ב2"),
             Tsubject(t_sub_id=28, teacher="hadar", subject="חינוך_ב2"),
             Tsubject(t_sub_id=29, teacher="hadar", subject="הנדסה_ב2"),
             ]

Aconstraints = [Aconstraint(a_con_id=1, subject="ספורט", h_quantity=2),
                Aconstraint(a_con_id=2, subject="אומנות", h_quantity=2),
                Aconstraint(a_con_id=3, subject="חשבון_א1", h_quantity=4),
                Aconstraint(a_con_id=4, subject="שפה_א1", h_quantity=10),
                Aconstraint(a_con_id=5, subject="מדעים_א1", h_quantity=2),
                Aconstraint(a_con_id=6, subject="חינוך_א1", h_quantity=2),
                Aconstraint(a_con_id=7, subject="הנדסה_א1", h_quantity=3),
                Aconstraint(a_con_id=8, subject="מוזיקה", h_quantity=1),
                Aconstraint(a_con_id=9, subject="חשבון_ג1", h_quantity=4),
                Aconstraint(a_con_id=10, subject="תנך_ג1", h_quantity=3),
                Aconstraint(a_con_id=11, subject="תורה_א1", h_quantity=2),
                Aconstraint(a_con_id=12, subject="מדעים_ג1", h_quantity=3),
                Aconstraint(a_con_id=13, subject="עברית_ג1", h_quantity=5),
                Aconstraint(a_con_id=14, subject="חינוך_ג1", h_quantity=2),
                Aconstraint(a_con_id=15, subject="גיאוגרפיה_ג1", h_quantity=2),
                Aconstraint(a_con_id=16, subject="הנדסה_ג1", h_quantity=3),
                Aconstraint(a_con_id=17, subject="אנגלית_ג1", h_quantity=2),
                Aconstraint(a_con_id=18, subject="חשבון_ד2", h_quantity=4),
                Aconstraint(a_con_id=19, subject="תנך_ד2", h_quantity=3),
                Aconstraint(a_con_id=21, subject="מדעים_ד2", h_quantity=3),
                Aconstraint(a_con_id=22, subject="עברית_ד2", h_quantity=5),
                Aconstraint(a_con_id=23, subject="חינוך_ד2", h_quantity=2),
                Aconstraint(a_con_id=24, subject="גיאוגרפיה_ד2", h_quantity=2),
                Aconstraint(a_con_id=25, subject="הנדסה_ד2", h_quantity=3),
                Aconstraint(a_con_id=26, subject="אנגלית_ד2", h_quantity=2),
                Aconstraint(a_con_id=27, subject="חשבון_ב2", h_quantity=5),
                Aconstraint(a_con_id=28, subject="שפה_ב2", h_quantity=7),
                Aconstraint(a_con_id=29, subject="מדעים_ב2", h_quantity=3),
                Aconstraint(a_con_id=30, subject="חינוך_ב2", h_quantity=2),
                Aconstraint(a_con_id=31, subject="הנדסה_ב2", h_quantity=3),
                Aconstraint(a_con_id=32, subject="תורה_ב2", h_quantity=4)
                ]

messeges = [Messeges(messege_id=1, teacher='ruti', classroom='א1')]

save(messeges)
save(Classrooms, Classroom)
save(Students, Student)
save(Events, Event)
save(Tsubjects, Tsubject)
save(Aconstraints, Aconstraint)
