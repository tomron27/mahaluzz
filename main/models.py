from django.db import models
import datetime
from django.contrib.auth.models import User, Group


class Classroom(models.Model):
    name = models.CharField(max_length=5, primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def create(self):
        self.save()

    @property
    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    parent1 = models.CharField(max_length=30)
    parent2 = models.CharField(max_length=30)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    birthday = models.DateField()

    def create(self):
        self.save()

    def __str__(self):
        return self.id


class Schedule(models.Model):
    schedule_id = models.CharField(max_length=10, primary_key=True)
    day_of_week = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.schedule_id


class Event(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    day = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()

    def create(self):
        self.save()

    def __str__(self):
        return self.name


class Tconstraint(models.Model):
    t_con_id = models.CharField(max_length=10, primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()
    priority = models.PositiveIntegerField()

    def create(self):
        self.save()

    def __str__(self):
        return self.t_con_id


class Tsubject(models.Model):
    t_sub_id = models.CharField(max_length=10, primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.t_sub_id

