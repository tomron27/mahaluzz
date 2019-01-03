from django.shortcuts import render, redirect
from .forms import LoginForm, MessageForm
from .user_auth import check_user
from django.contrib.auth.models import User, Group
from .models import *
from main.lp import Model
import itertools
import datetime
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

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
                user_Group = user.groups.all()[0]
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
                        classes_dict[class_x.name] = name_teacher.first_name
                    return master(request, master_name, classes_dict)
                #teacher_class =
                teacher_name = user_name[0][0]
                # return render(request, 'teacher.html', {'teacher_name': teacher_name})
                return redirect('teacher', teacher_name=teacher_name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})

def parent(request,parent_name,child_dict):
    return render(request, 'parent.html', {'parent_name': parent_name, 'child_dict': child_dict})

def master(request,master_name,classes_dict):
    return render(request, 'master.html', {'master_name': master_name, 'all_classes': classes_dict})

def teacher(request, teacher_name):
    if request.method == 'POST':
        print(request.POST)
        message_form = MessageForm(request.POST)
        message = request.POST.dict()
        print(type(message), message)
        print(message["textarea"])
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

def solve_and_save_schedule():
    print('Starting LP problem...')
    lp = Model()
    sol_status, sol = lp.solve()
    if sol_status == 'Optimal':
        print('Deleting old schedule...')
        Schedule.objects.all().delete()
        # insert dummy data to schedule
        print('Inserting dummy schedule to database...')
        cart = itertools.product(lp.DAYS, lp.HOURS, lp.CLASSES, repeat=1)
        i = 0
        for row in cart:
            sched_item = Schedule(schedule_id=i, day_of_week=row[0], hour=row[1], classroom=row[2], teacher='no_teacher', subject='חלון')
            sched_item.save()
            i += 1
        print('Inserting actual schedule to database...')
        for j, item in enumerate(sol):
            # Delete matching dummy schedule item
            to_del = Schedule.objects.filter(day_of_week=item[0], hour=item[1], classroom=item[3])
            to_del.delete()
            # Save new schedule data
            sched_item = Schedule(schedule_id=j+i, day_of_week=item[0], hour=item[1], classroom=item[3], teacher=item[4], subject=item[2])
            sched_item.save()
        print('Schedule Saved')

def get_current_weekdates():
    today = datetime.date.today()
    last_sunday = today - datetime.timedelta(days=today.weekday()+1)
    raw_dates = [last_sunday + datetime.timedelta(days=i) for i in range(6)]
    dates = []
    for x in raw_dates:
        dates.append((_(x.strftime("%A"))) + ' ' + x.strftime("%d/%m/%y"))
    return dates

def constraints(request, teacher_name):
    if request.method == 'POST':
        con_dict = request.POST.dict()
        con_dict.pop("csrfmiddlewaretoken", None)
        max_id = 0
        try:
            max_id = int(Tconstraint.objects.latest('t_con_id').t_con_id)
        except:
            print('Tconstraints is empty')
        user = User.objects.get(first_name=teacher_name)
        # Check for existing constraint and delete
        to_del = Tconstraint.objects.filter(teacher=user.username)
        if to_del:
            message = to_del.delete()
            print('Deleted {} existing constraints for username = "{}"'.format(message[0], user.username))
        for i, x in enumerate(con_dict):
            Tcons = Tconstraint(t_con_id=max_id+i, teacher=user.username, day_of_week=int(x[1]), hour=int(x[3]), priority=int(con_dict[x]))
            Tcons.save()
        print('Inserted {} constraints for username = "{}"'.format(len(con_dict), user.username))
    return render(request, 'constraint.html')

def constraints_test(request, teacher_name=None):
    return render(request, 'constraints_test.html', {'teacher_name': teacher_name})

