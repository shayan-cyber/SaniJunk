from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Locations(models.Model):
    name = models.CharField(max_length=200)
    locator_user = models.ForeignKey(User,on_delete=models.CASCADE)
    locator_mail = models.CharField(max_length=200)
    sanitized = models .CharField(max_length=200, default="No")
    sanitizer_mail = models.CharField(max_length=200, blank = True, null=True)
    garbageType = models.CharField(max_length=50)
    coordinates_lat = models.CharField(max_length=200)
    coordinates_lng =models.CharField(max_length=200)
    saturation = models.CharField(max_length = 200)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name) 
class NewsLetter(models.Model):
    email = models.CharField(max_length=300)
    def __str__(self):
        return str(self.email)

class Quiz(models.Model):
    question = models.CharField(max_length=400)
    opt1 = models.CharField(max_length=300)
    opt2 = models.CharField(max_length=300)
    opt3 = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.question)

    