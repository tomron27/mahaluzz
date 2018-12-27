from main.models import *


def save(objects, table=None):
    if table is not None:
        table.objects.all().delete()
    for obj in objects:
        obj.save()


Classrooms = [Classroom(name="א1", teacher="ruti"), Classroom(name="ג1", teacher="shush")]

Students = [Student(id="302077633", first_name="שיר", last_name="כהן", parent1="haimcohen", parent2="dorit",
            classroom="א1", birthday='2003-01-17'), Student(id="302077634", first_name="דורון", last_name="כהן"
            , parent1="haimcohen", parent2="dorit", classroom="ג1", birthday='2005-01-20'),
            Student(id="302077635", first_name="תום", last_name="כהן", parent1="haimcohen", parent2="dorit"
            , classroom="ג1", birthday='2005-01-20'), Student(id="302077635", first_name="נעמי", last_name="טננבאום",
            parent1="shaolm", parent2="noga", classroom="א1", birthday='2003-04-20')]

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


save(Classrooms)
save(Students)
save(Events)
save(Tsubjects)
