from django.shortcuts import render
from .forms import LoginForm
from .user_auth import check_user
from django.contrib.auth.models import User, Group
from .models import *
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
                    child_list1 = Student.objects.filter(parent1=user)
                    child_list2 = Student.objects.filter(parent2=user)
                    child_list_query = child_list1.union(child_list2)
                    child_dict = {}
                    for query in child_list_query:
                        child_dict[query.first_name] = query.classroom
                        print(query.first_name)
                    print(child_dict)
                    parent_name = user_name[0][0]
                    return render(request, 'parent.html', {'parent_name': parent_name, 'child_dict': child_dict})
                if (user_Group.name == 'Master'):
                    master_name = user_name[0][0]
                    all_classes = Classroom.objects.order_by('name')
                    classes_dict = {}
                    for class_x in all_classes:
                        classes_dict[class_x.name]=class_x.teacher
                    print(classes_dict)
                    return render(request, 'master.html', {'master_name': master_name, 'all_classes': classes_dict})
                #teacher_class =
                teacher_name = user_name[0][0]
                return render(request, 'teacher.html', {'teacher_name': teacher_name})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})
