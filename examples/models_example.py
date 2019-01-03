from django.db import models
import datetime

default_lesson_length = 45
max_len = 255

# Location for a lesson
class Classroom(models.Model):
    name = models.CharField(max_length=max_len)
    capacity = models.PositiveIntegerField(blank=True)

    def create(self):
        self.save()

    def __str__(self):
        return self.name


# Mother class of a student
class Class(models.Model):
    name = models.CharField(max_length=max_len)
    classroom = models.CharField(max_length=max_len, blank=True)

    def create(self):
        self.save()

    def __str__(self):
        return self.name


# Abstract event base class
class AbstractEvent(models.Model):
    start_time = models.DateTimeField()
    length = models.DurationField(default=datetime.timedelta(minutes=default_lesson_length))

    class Meta:
        abstract = True


# Lesson event
class Lesson(AbstractEvent):
    title = models.CharField(max_length=max_len)
    _class = models.CharField(max_length=max_len, blank=True)
    location = models.CharField(max_length=max_len, blank=True)
    has_hw = models.BooleanField(default=False)
    # teacher

    def create(self):
        self.save()

    def __str__(self):
        return self.title
