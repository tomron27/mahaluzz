from django.db import models
import datetime
from django.contrib.auth.models import User, Group


class Classroom(models.Model):
    class_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    parent1 = models.CharField(max_length=30)
    parent2 = models.CharField(max_length=30)
    classroom = models.CharField(max_length=5)
    birthday = models.DateField()

    def create(self):
        self.save()

    def __str__(self):
        return self.id


class Schedule(models.Model):
    schedule_id = models.PositiveIntegerField(primary_key=True)
    day_of_week = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()
    classroom = models.CharField(max_length=5)
    teacher = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.subject + '_' + self.classroom


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
    t_con_id = models.PositiveIntegerField(primary_key=True)
    teacher = models.CharField(max_length=30)
    day_of_week = models.PositiveIntegerField()
    hour = models.PositiveIntegerField()
    priority = models.PositiveIntegerField()

    def create(self):
        self.save()

    def __str__(self):
        return self.t_con_id


class Aconstraint(models.Model):
    a_con_id = models.PositiveIntegerField(primary_key=True)
    subject = models.CharField(max_length=30)
    h_quantity = models.PositiveIntegerField()

    def create(self):
        self.save()

    def __str__(self):
        return self.a_con_id


class Tsubject(models.Model):
    t_sub_id = models.CharField(max_length=10, primary_key=True)
    teacher = models.CharField(max_length=3)
    subject = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.t_sub_id

class Messages(models.Model):
    message = models.PositiveIntegerField(primary_key=True)
    teacher = models.CharField(max_length=31)
    classroom = models.CharField(max_length=5)

    def create(self):
        self.save()

    def _str_(self):
        return str(self.message)