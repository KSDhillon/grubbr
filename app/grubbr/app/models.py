from django.db import models

class User(models.Model):
    email = model.EmailField(max_length=150, unique=True)
    password = model.CharField(max_length=200)
    street = model.CharField(max_length=300)
    city = model.CharField(max_length=100)
    state = model.CharField(max_length=50)
    zipcode = model.CharField(max_length=5)

class Meal(models.Model):
    cook = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    portions = models.IntegerField(default=1)
    
