from django.shortcuts import render, redirect
from .forms import LoginForm, MessageForm
from .user_auth import check_user
from django.contrib.auth.models import User, Group
from .models import *
from main.lp import Model
import itertools
import datetime
from django.http import HttpResponse
from threading import Thread
from time import sleep
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _


def login(request):
    has_errors = message = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            has_errors, message, user_queryset = check_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if has_errors:
                # Error - Login Again
                return render(request, 'registration/login.html',
                                {'form': form, 'has_errors': has_errors, 'message': message})
            else:
                # Resolve entity
                uid = user_queryset.values_list('id')
                user = User.objects.get(id=uid[0][0])
                user_group = user.groups.all()[0]
                if user_group.name == 'Parents':
                    return redirect('parent', username=user.username)
                if user_group.name == 'Master':
                    return redirect('master', username=user.username, status='normal')
                if user_group.name == 'Teacher':
                    return redirect('teacher', username=user.username)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})


def parent(request, username):
    user_data = User.objects.get(username=username)
    dates = get_current_weekdates()
    child_list1 = Student.objects.filter(parent1=username)
    child_list2 = Student.objects.filter(parent2=username)
    child_list_query = child_list1.union(child_list2)
    data = {}
    for query in child_list_query:
        child_name = query.first_name
        classroom = query.classroom
        schedule = {'dates': dates, 'schedule_data': return_schedule(classroom, 'Classroom')}
        messages = {}
        all_messages = return_messeges(classroom, messages)
        #print('class=', classroom, 'messeges=', all_messages)
        user_name = get_base_teacher(classroom)
        print(user_name)
        teacher_name = User.objects.get(username=user_name).first_name
        #print(teacher_name)
        data[child_name] = {'name': child_name, 'classroom': classroom, 'schedule': schedule, 'messages': all_messages, 'teacher_name':teacher_name}
    return render(request, 'parent.html', {'parent_name': user_data.first_name, 'data': data})


def master(request, username, status):
    user_data = User.objects.get(username=username)
    dates = get_current_weekdates()
    all_classes = Classroom.objects.order_by('name')
    data = {}
    for class_x in all_classes:
        teacher_name = User.objects.get(username=class_x.teacher)
        messeges = {}
        all_messages = return_messeges(class_x.name, messeges)
        # print(all_messages)
        schedule = {'dates': dates, 'schedule_data': return_schedule(class_x.name, 'Classroom')}
        data[class_x.name] = {'name': teacher_name, 'classroom': class_x.name, 'schedule': schedule,
                              'messages': all_messages}

    if status == 'done':
        print('done!')
        status = Status.objects.get(id=0).status
        redirect('master', username=username, status=status)

    if request.method == 'POST':
        if 'start_schedule' in request.POST.dict():
            if request.POST.dict()['start_schedule'] == 'true':
                t = Thread(target=master_scheduling, args=(request, username, data))
                t.start()
                return redirect('master', username=username, status='in_progress')

        #print(request.POST)
        message_form = MessageForm(request.POST)
        message = request.POST.dict()
        base_class = get_base_class()
        for class_name in base_class:
            max_id = 0
            try:
                max_id = int(Messages.objects.latest('message_id').message_id)
            except:
                print('Messeges is empty')
            Tmessage = Messages(message_id=max_id+1, teacher=username, classroom=class_name, message=message["textarea"])
            Tmessage.save()
    return render(request, 'master.html', {'master_name': user_data.first_name, 'data': data, 'status': status})



def teacher(request, username):
    user_data = User.objects.get(username=username)
    dates = get_current_weekdates()
    if request.method == 'POST':
        print(request.POST)
        message_form = MessageForm(request.POST)
        message = request.POST.dict()
        base_class = get_base_class(username)
        for class_name in list(base_class):
            max_id = 0
            try:
                max_id = int(Messages.objects.latest('message_id').message_id)
            except:
                print('Messeges is empty')
            Tmessage = Messages(message_id=max_id+1, teacher=username, classroom=class_name[1], message=message["textarea"])
            Tmessage.save()
    schedule = {'dates': dates, 'schedule_data': return_schedule(username, 'Teacher')}
    return render(request, 'teacher.html', {'username': username, 'teacher_name': user_data.first_name, 'schedule': schedule})


def constraints(request, username):
    user_data = User.objects.get(username=username)
    if request.method == 'POST':
        if 'submit' in request.POST.dict():
            con_dict = request.POST.dict()
            con_dict.pop("csrfmiddlewaretoken", None)
            max_id = 0
            try:
                max_id = int(Tconstraint.objects.latest('t_con_id').t_con_id)
            except:
                print('Tconstraints is empty')
            # Check for existing constraint and delete
            to_del = Tconstraint.objects.filter(teacher=user_data.username)
            if to_del:
                message = to_del.delete()
                print('Deleted {} existing constraints for username = "{}"'.format(message[0], user_data.username))
            for i, x in enumerate(con_dict):
                if x[0] == 'M':
                    Tcons = Tconstraint(t_con_id=max_id+i, teacher=user_data.username, day_of_week=int(x[1]), hour=int(x[3]), priority=int(con_dict[x]))
                    Tcons.save()
            print('Inserted {} constraints for username = "{}"'.format(len(con_dict), user_data.username))
            return redirect('teacher', username=username)
        if 'back' in request.POST.dict():
            print(request.POST.dict())
            return redirect('teacher', username=username)
    return render(request, 'constraint.html', {'username': username})


def return_messeges(entity, messages):
    #print(type(entity.name),entity.name)
    messages_query = Messages.objects.filter(classroom=entity)
    for message in messages_query.values_list():
        #print(type(message[2]), message[2])
        if entity not in messages:
            messages[entity] = [message[3]]
        else:
            messages[entity].append(message[3])
    return messages


def return_schedule(entity, entity_type):
    if entity_type == 'Classroom':
        schedule_queryset = Schedule.objects.filter(classroom=entity).order_by('hour', 'day_of_week')
    elif entity_type == 'Teacher':
        schedule_queryset = Schedule.objects.filter(teacher=entity).order_by('hour', 'day_of_week')

    lesson_dict = {}    # {Entity: Entity Lessons (schedule objects)}
    groups = itertools.groupby(schedule_queryset, lambda x: x.hour)
    for key, group in groups:
        if key not in lesson_dict:
            lesson_dict[key] = list(group)
        else:
            lesson_dict[key] += list(group)

    hours_with_lessons = [{'hour': k, 'lesson': lesson_dict[k]} for k in lesson_dict]
    return hours_with_lessons


def master_scheduling(request, username, data):
    status = solve_and_save_schedule()
    return redirect('master', username=username, status=status)


def solve_and_save_schedule():
    print('Starting LP problem...')
    lp = Model()
    sol_status, sol = lp.solve()
    if sol_status != 'Optimal':
        print('Problem infeasible. Aborting scheduling...')
        query = Status.objects.all()
        query.delete()
        Status(id=0, status='error').save()
        print('Deleted problem status from DB')
        return 'error'
    else:
        print('Deleting old schedule...')
        Schedule.objects.all().delete()
        # insert dummy data to schedule
        print('Inserting dummy schedule to database...')
        class_cart = itertools.product(lp.DAYS, lp.HOURS, lp.CLASSES, repeat=1)
        teacher_cart = itertools.product(lp.DAYS, lp.HOURS, lp.TEACHERS, repeat=1)
        i = 0
        for row in class_cart:
            if row[1] == 4:
                sched_item = Schedule(schedule_id=i, day_of_week=row[0], hour=row[1], classroom=row[2], subject='הפסקה')
            else:
                sched_item = Schedule(schedule_id=i, day_of_week=row[0], hour=row[1], classroom=row[2], subject='')
            sched_item.save()
            i += 1
        for row in teacher_cart:
            if row[1] == 4:
                sched_item = Schedule(schedule_id=i, day_of_week=row[0], hour=row[1], teacher=row[2], subject='הפסקה')
            else:
                sched_item = Schedule(schedule_id=i, day_of_week=row[0], hour=row[1], teacher=row[2], subject='')
            sched_item.save()
            i += 1
        print('Inserting actual schedule to database...')
        for j, item in enumerate(sol):
            # Delete matching dummy schedule item (classes + teachers)
            to_del = Schedule.objects.filter(day_of_week=item[0], hour=item[1], classroom=item[3])
            to_del.delete()
            to_del = Schedule.objects.filter(day_of_week=item[0], hour=item[1], teacher=item[4])
            to_del.delete()
            # Save new schedule data
            sched_item = Schedule(schedule_id=j+i, day_of_week=item[0], hour=item[1], classroom=item[3], teacher=item[4], subject=item[2])
            sched_item.save()
        print('Schedule Saved')
        query = Status.objects.all()
        query.delete()
        Status(id=0, status='success').save()
        print('Saved problem status to DB')
    return 'success'

def get_current_weekdates():
    today = datetime.date.today()
    if today.weekday() != 6:
        last_sunday = today - datetime.timedelta(days=today.weekday()+1)
    else:
        last_sunday = today
    raw_dates = [last_sunday + datetime.timedelta(days=i) for i in range(6)]
    dates = []
    for x in raw_dates:
        dates.append((_(x.strftime("%A"))) + ' ' + x.strftime("%d/%m/%y"))
    return dates


def get_base_teacher(classroom):
    teacher_list = Classroom.objects.values('teacher').annotate(Count('class_id')).filter(class_id__count=1)
    for arg in teacher_list:
        #print('args=', arg['teacher'],type(arg))
        classroom_teacher = Classroom.objects.get(teacher=arg['teacher'])
        if classroom == classroom_teacher.name:
            return arg['teacher']

def get_base_class(teacher_name=None):
    if teacher_name is None:
        all_classes = Classroom.objects.order_by('name')
        xlist = all_classes.values_list()
        xlist = [x[1] for x in xlist]
        xlist = list(set(xlist))
        return xlist
    else:
        class_list = Classroom.objects.filter(teacher=teacher_name)
        return class_list.values_list()

def report_stud(request):
    return render(request, 'stu_names.html')


def report_birth(request):
    return render(request, 'stu_birth.html')

