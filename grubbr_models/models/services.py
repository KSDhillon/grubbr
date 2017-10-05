from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import *

def message(success, result):
    res = {
        'success': success,
        'result': result
    }
    return JsonResponse(res)

@csrf_exempt
def create_user(request):
    if (request.method != 'POST'):
        return message(False, "Cannot " + request.method + " to" + request.path)
    else:
        #extracting body elements
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        #validation elements
        if (not email or not password or not first_name or not last_name):
            return message(False, "All fields must be provided to create a user.")

        #hashing password
        encrypted_password = make_password(password)

        user = User(
            email=email,
            password=encrypted_password,
            first_name=first_name,
            last_name=last_name
        )
        try:
            user.save()
        except:
            return message(False, "There was an error saving user to database.")
        return message(True, "User was created.")

@csrf_exempt
def create_meal(request):
    if (request.method != 'POST'):
        return message(False, "Cannot " + request.method + " to" + request.path)
    else:
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        portions = request.POST['portions']

        #validate fields
        if(not name or not price or not description or not portions):
            return message(False, "All fields must be provided to create a meal.")
            
        meal = Meal(
            name=request.POST['name'],
            price=request.POST['price'],
            description=request.POST['description'],
            portions=request.POST['portions'],
        )
        try:
            meal.save()
        except:
            return message(False, "There was an error saving user to database.")
        return message(True, "Meal was created.")

@csrf_exempt
def rud_user_by_id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return message(False, "User Does Not Exist")
    if (request.method == 'GET'):
        return message(True, user.to_json())
    elif (request.method == 'POST'):
        for field, value in request.POST.items():
            setattr(user, field, value)
        user.save()
        return message(True, "User was updated")
    elif (request.method == 'DELETE'):
        user.delete()
        return message(True, "User was deleted.")
    else:
        return message(False, "Cannot " + request.method + " to" + request.path)

@csrf_exempt
def rud_meal_by_id(request, meal_id):
    try:
        meal = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        return message(False, "Meal Does Not Exist")
    if (request.method == 'GET'):
        return message(True, meal.to_json())
    elif (request.method == 'POST'):
        for field, value in request.POST.items():
            setattr(user, field, value)
        meal.save()
        return message(True, "Meal was updated")
    elif (request.method == 'DELETE'):
        meal.delete()
        return message(True, "Meal was deleled.")
    else:
        return message(False, "Cannot " + request.method + " to" + request.path)
