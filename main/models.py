from django.db import models
import datetime


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    parent1 = models.CharField(max_length=30)
    parent2 = models.CharField(max_length=30, blank=True)
    classroom = models.CharField(max_length=5)
    birthday = models.DateField()

    def create(self):
        self.save()

    def __str__(self):
        return self.id

class Classroom(models.Model):
    name = models.CharField(max_length=5, primary_key=True)
    teacher = models.CharField(max_length=30)

    def create(self):
        self.save()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    #day_of_week = models.PositiveIntegerField(primary_key=True)
    #hour = models.PositiveIntegerField(primary_key=True)
    #classroom= models.CharField(max_length=5, primary_key=True)
    # subject= ************

    def create(self):
        self.save()



class Event(models.Model):
    name= models.CharField(max_length=60)
    day= models.PositiveIntegerField()
    month= models.PositiveIntegerField()
    hour = models.PositiveIntegerField()

    def create(self):
        self.save()

    def __str__(self):
        return self.name


# class Tconstraints(models.Model):
#     teacher= models.CharField(max_length=30, primary_key=True)
#     day_of_week = models.PositiveIntegerField(primary_key=True)
#     hour = models.PositiveIntegerField(primary_key=True)
#     #priority= models.PositiveIntegerField(options=(0,1,2))
#
#     def create(self):
#         self.save


# class Tsubjects(models.Model):
#     teacher = models.CharField(max_length=30, primary_key=True)
#     subject = models.CharField(max_length=30, primary_key=True)
#
#     def create(self):
#         self.save()