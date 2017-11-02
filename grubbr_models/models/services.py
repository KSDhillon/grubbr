from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import datetime
from datetime import timedelta
from .models import *

def message(success, result):
    res = {
        'success': success,
        'result': result
    }
    return JsonResponse(res)

@csrf_exempt
def create_user(request):
    if (request.method == 'POST'):
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
        except IntegrityError:
            return message(False, "Account with this email already exists.")
        except:
            return message(False, "There was an error creating this user.")
        return message(True, "User was created.")
    elif (request.method == 'GET'):
        users = User.objects.all()
        result = []
        for user in users:
            result.append(user.to_json())
        return message(True, result)
    else:
        return message(False, "Cannot " + request.method + " to" + request.path)

@csrf_exempt
def create_meal(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        portions = request.POST['portions']

        #validate fields
        if (not name or not price or not description or not portions):
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
        return message(True, meal.to_json())
    elif (request.method == 'GET'):
        meals = Meal.objects.all()
        result = []
        for meal in meals:
            result.append(meal.to_json())
        return message(True, result)
    else:
        return message(False, "Cannot " + request.method + " to" + request.path)

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
            if field == 'password':
                setattr(user, field, make_password(value))
                continue
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
            setattr(meal, field, value)
        meal.save()
        return message(True, "Meal was updated")
    elif (request.method == 'DELETE'):
        meal.delete()
        return message(True, "Meal was deleled.")
    else:
        return message(False, "Cannot " + request.method + " to" + request.path)

def create_auth():
    while True:
        authenticator = hmac.new(
            key = settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256',
        ).hexdigest()
        try:
            auth = Authenticator.objects.get(pk=authenticator)
        except Authenticator.DoesNotExist:
            return authenticator

# Attempts to login using email and password, returns authenticator string if valid login
@csrf_exempt
def login_user(request):
    if request.method == 'GET':
        return message(False, "Cannot make GET request for login")
    if (not request.POST['email'] or not request.POST['password']):
        return message(False, "An email or password was not provided")
    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        return message(False, "User Does Not Exist")
    if not user.check_password(request.POST['password']):
        return message(False, "Email and password do not match")

    # Username and password match, create authenticator
    auth = Authenticator(
        user_id=user.email,
        authenticator = create_auth()
    )

    try:
        auth.save()
    except:
        return message(False, "Could not create authenticator")

    return message(True, auth.authenticator)

@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        return message(False, "Cannot make GET request for logout")

    try:
        auth = Authenticator.objects.get(pk=request.POST['auth'])
    except:
        return message(False, "Authenticator does not exis")
    auth.delete()

    return message(True, "User logged out")

def authenticate(request):
    if request.method == 'GET':
        return message(False, "Cannot make GET request for authentication")

    if not request.POST['auth']:
        return message(False, "No authenticator passed")

    try:
        auth = Authenticator.objects.get(pk=request.POST['auth'])
    except Authenticator.DoesNotExist:
        return message(False, "Authentication not recognized")

    created = auth.date_created
    now = datetime.datetime.now(created.tzinfo)
    timePassed = now - created
    if timePassed.seconds > 600: # Timeout seconds: 10 min
        auth.delete()
        return message(False, "Timed out")
    else: # Update auth for another 10 min
        auth.date_created = now
        auth.save()

    return message(True, "Authentication valid")
