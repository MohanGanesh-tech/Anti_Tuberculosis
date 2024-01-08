from django.db import models
from datetime import datetime

# Create your models here.
class user(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    dob =  models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class survey(models.Model):
    uid = models.IntegerField()
    answers = models.CharField(max_length=100)
    group = models.IntegerField()
    knowledge = models.CharField(max_length=200)
    datetime =  models.DateTimeField(auto_now=True)