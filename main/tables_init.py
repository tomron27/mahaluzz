from main.models import *

def save(objects, table=None):
    if table is not None:
        table.objects.all().delete()
    for obj in objects:
        obj.save()

Classrooms = [Classroom(name="א1", teacher="ruti"), Classroom(name="ג1", teacher="shush")]

Students = [Student(id="302077633", first_name="shir", last_name="cohen", parent1="haimcohen", parent2="dorit", classroom="א1", birthday='2003-01-17'),
            Student(id="302077634", first_name="doron", last_name="cohen", parent1="haimcohen", parent2="dorit", classroom="ג1",birthday='2005-01-20')]

Events = [Event(name= 'טקס ט"ו בשבת',day=14, month=1, hour=8)]


save(Classrooms, Classroom)
save(Students, Student)
save(Events, Event)
