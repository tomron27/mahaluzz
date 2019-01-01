from django.shortcuts import render
from .forms import LoginForm
from .user_auth import check_user
from django.contrib.auth.models import User, Group
from .models import *
import itertools
import datetime
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from main.tables_init import *

# Create your views here.

def login(request):
    # if this is a POST request we need to process the form data
    has_errors = message = False
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            has_errors, message, user_queryset = check_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if has_errors:
                # Error - Login Again
                return render(request, 'registration/login.html',
                                {'form': form, 'has_errors': has_errors, 'message': message})
            else:
                dates = get_current_weekdates()
                uid = user_queryset.values_list('id')
                user_name = user_queryset.values_list('first_name')
                user = User.objects.get(id=uid[0][0])
                print(user_queryset.values())
                print(user_name)
                print(user)
                print(user_name[0][0])
                print(user.groups.all()[0])
                user_Group = user.groups.all()[0]
                print(type(user_Group))
                print(user_Group.name)
                if (user_Group.name == 'Parents'):
                    parent_name = user_name[0][0]
                    child_list1 = Student.objects.filter(parent1=user)
                    child_list2 = Student.objects.filter(parent2=user)
                    child_list_query = child_list1.union(child_list2)
                    children_dict = {}
                    for query in child_list_query:
                        child_name = query.first_name
                        classroom = query.classroom
                        schedule = {'dates': dates, 'schedule_data': return_schedule(classroom, 'Classroom')}
                        children_dict[child_name] = {'name': child_name, 'classroom': classroom, 'schedule': schedule}
                    return render(request, 'parent.html', {'parent_name': parent_name, 'children_dict': children_dict})
                if (user_Group.name == 'Master'):
                    master_name = user_name[0][0]
                    all_classes = Classroom.objects.order_by('name')
                    classes_dict = {}
                    for class_x in all_classes:
                        name_teacher = User.objects.get(username=class_x.teacher)
                        print(name_teacher.first_name)
                        classes_dict[class_x.name] = name_teacher.first_name
                    print(classes_dict)
                    return master(request, master_name, classes_dict)
                #teacher_class =
                teacher_name = user_name[0][0]
                return render(request, 'teacher.html', {'teacher_name': teacher_name})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})

def parent(request,parent_name,child_dict):
    return render(request, 'parent.html', {'parent_name': parent_name, 'child_dict': child_dict})

def master(request,master_name,classes_dict):
    return render(request, 'master.html', {'master_name': master_name, 'all_classes': classes_dict})


def teacher(request, teacher_name):
    print(request.POST)
    if request.method == 'POST' and 'btnform1' in request.POST:
        return constraints(request, teacher_name)
    return render(request, 'teacher.html', {'teacher_name': teacher_name})

def return_schedule(entity, entity_type):
    lesson_dict = {}    # {Entity: Entity Lessons}
    if entity_type == 'Classroom':
        schedule_queryset = Schedule.objects.filter(classroom=entity).order_by('day_of_week', 'hour')
    elif entity_type == 'Teacher':
        schedule_queryset = Schedule.objects.filter(teacher=entity).order_by('day_of_week', 'hour')

    groups = itertools.groupby(schedule_queryset, lambda x: x.day_of_week)
    for key, group in groups:
        if key not in lesson_dict:
            lesson_dict[key] = list(group)
        else:
            lesson_dict[key] += list(group)

    hours_with_lessons = [{'hour': k, 'lesson': lesson_dict[k]} for k in lesson_dict]
    return hours_with_lessons

def get_current_weekdates():
    today = datetime.date.today()
    last_sunday = today - datetime.timedelta(days=today.weekday()+1)
    raw_dates = [last_sunday + datetime.timedelta(days=i) for i in range(6)]
    dates = []
    for x in raw_dates:
        dates.append((_(x.strftime("%A"))) + ' ' + x.strftime("%d/%m/%y"))
    return dates

def constraints(request, teacher_name):
    print(teacher_name)
    if request.method == 'POST':
        con_dict = request.POST.dict()
        con_dict.pop("csrfmiddlewaretoken", None)
        Tconstraints = []
        for i,x in enumerate(con_dict):
            x_list = list(x)
            print(x_list)
            Tcons = Tconstraint(t_con_id=i, teacher=teacher_name, day_of_week=x_list[1], hour=x_list[3], priority=con_dict[x])
            Tcons.save()
        #save(Tconstraints)
    return render(request, 'constraint.html')

def constraints_test(request, teacher_name=None):
    return render(request, 'constraints_test.html', {'teacher_name': teacher_name})

