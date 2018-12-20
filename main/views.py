from django.shortcuts import render
from .forms import LoginForm
from .user_auth import check_user
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# Create your views here.

def login(request):
    # Check if already logged in then redirect to home page
    username = None
    if 'username' in request.session:
        username = request.session['username']
        return render(request, 'home.html', {'username': username})

    # Check existence of user in django user database
    has_errors = message = False
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            has_errors, message = check_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if has_errors:
                return render(request, 'registration/login.html',
                                {'form': form, 'has_errors': has_errors, 'message': message})
            else:
                request.session['username'] = username = form.cleaned_data['username']
                return render(request, 'home.html', {'username': username})

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'has_errors': has_errors, 'message': message})

def logout(request):
    # TODO - proper logout (with cookie deletion)
    return HttpResponse('bye')