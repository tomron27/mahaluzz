from django.shortcuts import render
from .forms import LoginForm
from .user_auth import check_user
from django.contrib.auth.models import User, Group
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
            has_errors, message,user_queryset = check_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if has_errors:
                # Error - Login Again
                return render(request, 'registration/login.html',
                                {'form': form, 'has_errors': has_errors, 'message': message})
            else:
                #TODO: Jump to page by User Group

                uid = user_queryset.values_list('id')
                #print(uid)
                #print(uid[0][0])
                user = User.objects.get(id=uid[0][0])
                print(user)
                print(user.groups.all()[0])
                user_Group = user.groups.all()[0]
                if (user_Group == 'Parents'):
                    return render(request, 'home.html')
                if (user_Group == 'Master'):
                    return render(request, 'home.html')
                return render(request, 'home.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})
