"""SaniJunk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views 

urlpatterns = [
    path('signup_home', views.signup,name='signup_home'),
    # path('signup_home', views.signup_home,name=''),
    path('login', views.user_login,name='login'),
    path('logout', views.user_logout,name='logout'),
    path('', views.home, name='home'),
    path('add_location', views.add_location, name="add_location"),
     path('details/<int:pk>', views.details, name="details"),
     path('sanitize/<int:pk>', views.sanitize, name="sanitize"),
     path('verify/<int:pk>', views.verify, name="verify"),
     path('list', views.list,name='list'),
     path('newsletter', views.newsletter,name='newsletter'),
     path('founders', views.founders,name='founders'),
     path('quiz', views.quiz, name="quiz"),
    #  path('dat', views.dat, name='data')
    #  path('test', views.test, name="test")
]
