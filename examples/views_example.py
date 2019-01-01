from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from .models import *
from django.db.models.functions import Cast, TruncSecond, TruncMinute, ExtractHour, ExtractMinute
from django.db.models import DateTimeField, TimeField, CharField
from django_mahaluzz import settings
import datetime
import itertools
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def extract_date(entity):
    return entity.start_time.date()

def extract_time(entity):
    return entity.strftime("%H:%M")


start_hour = 8
start_minute = 0
day = 2
month = 12
year = 2018

def home(request):

    # Extract dates in <day_name> <dd/mm/yy> format
    # TODO - Add current week filter
    dates = [(_(x.strftime("%A")) + ' ' + x.strftime("%d/%m/%y"))
             for x in Lesson.objects.dates('start_time', 'day')]

    # Query a {hour: [lesson1, lesson2, ..]} dict
    lesson_dict = {}

    # Query example:
    result = Lesson.objects.order_by('start_time')

    groups = itertools.groupby(result, lambda x: x.start_time.strftime("%H:%M"))
    for key, group in groups:
        if key not in lesson_dict:
            lesson_dict[key] = list(group)
        else:
            lesson_dict[key] += list(group)

    hours_with_lessons = [{'hour': k, 'lesson': lesson_dict[k]} for k in lesson_dict]

    context = {'dates': dates, 'hours_with_lessons': hours_with_lessons}

    # return HttpResponse(dates)
    return render(request, 'schedule/home.html', context)


