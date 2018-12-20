from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('', views.home, name='schedule-home'),
    # path('language/', views.lang, name='schedule-lang-test'),
    # path('', LoginView.as_view()),
    # path('', views.formView, name='main-form_view'),
    path('', views.login, name='main-login'),
    path('logout', views.logout, name='main-logout'),
    # path('schedule', views.schedule, name='main-schedule'),
    # path('home', views.home, name='main-home')
    # path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginViews.as_views(    template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutViews.as_views(), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()