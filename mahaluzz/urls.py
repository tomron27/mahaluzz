"""mahaluzz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.login, name='login'),
    # path('', include('main.urls'), name='login'),
    path('parent/<str:username>', main_views.parent, name='parent'),
    path('master/<str:username>/<str:status>', main_views.master, name='master'),
    path('teacher/<str:username>/', main_views.teacher, name='teacher'),
    path('constraint/<str:username>/', main_views.constraints, name='constraint'),
    path('stu/', main_views.report_stud, name='stu'),
    path('birth/', main_views.report_birth, name='birth'),
]
