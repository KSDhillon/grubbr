from django.db import models

class User(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def to_json(self):
        return {
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

class Meal(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=500)
    portions = models.PositiveIntegerField(default=1)

    def to_json(self):
        return {
            'price': self.price,
            'name': self.price,
            'description': self.description,
            'portions': self.portions,
        }
