from django.conf.urls import url, include
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name='index'),
    path('login',views.index,name='login'),
    path('logout',views.logout,name='logout'),
    path('signuppage',views.signuppage,name="signuppage"),
    path('checkotp',views.checkotp,name='checkotp'),
    path('resendotp',views.resendotp,name='resendotp'),

    path('home',views.home,name="home"),
    path('usersignup',views.usersignup,name="usersignup"),
    path('userlogin',views.userlogin,name="userlogin"),

    path('survey',views.surveypage,name="survey"),
    path('survey_form',views.survey_form,name="survey_form"),


    # admin
    path('admin',views.admin,name='admin'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('adminlogout',views.adminlogout,name='adminlogout'),
    path('downloadreport',views.downloadreport,name='downloadreport'),

    path('surveyresult',views.surveyresult,name='surveyresult'),
    path('statistics',views.statistics,name='statistics'),

    path('reportsendgmail',views.reportsendgmail,name='reportsendgmail'),



]