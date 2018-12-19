from django.shortcuts import render
from .forms import LoginForm
from .user_auth import check_user
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# Create your views here.

def login(request):
    # if this is a POST request we need to process the form data
    has_errors = message = False
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # check whether it's valid:
        if form.is_valid():
            has_errors, message = check_user(username, password)
            print(has_errors, message)
            if has_errors:
                return render(request, 'registration/login.html',
                                {'form': form, 'has_errors': has_errors, 'message': message})
            else:
                return render(request, 'home.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})
