from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)

class Meal(models.Model):
    cook = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ManytoManyField(User)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    portions = models.IntegerField(default=1)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    pickup_time_start = models.DateTimeField()
    pickup_time_end = models.DateTimeField()
