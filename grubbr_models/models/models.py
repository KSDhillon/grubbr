from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
import os
import hmac

class User(AbstractBaseUser):
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def to_json(self):
        return {
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'id': self.id,
        }

class Meal(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=500)
    portions = models.PositiveIntegerField(default=1)

    def to_json(self):
        return {
            'price': self.price,
            'name': self.name,
            'description': self.description,
            'portions': self.portions,
            'id': self.id,
        }



class Authenticator(models.Model):
    user_id = models.CharField(max_length=200) # user email
    authenticator = models.CharField(primary_key=True, max_length = 200)
    date_created = models.DateTimeField(auto_now_add=True)

# def create_auth():
#     while True:
#         authenticator = hmac.new(
#             key = settings.SECRET_KEY.encode('utf-8'),
#             msg = os.urandom(32),
#             digestmod = 'sha256',
#         ).hexdigest()
#
#         auth = Authenticator.objects.get(pk=authenticator)
#         if auth.DoesNotExist:
#             return authenticator
