from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.request
import urllib.parse
from django.template import loader
import json
from . import forms

def home(request):
    req = urllib.request.Request('http://exp-api:8000/api/meals')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(resp_json)
    context = {
        'data': res['result']['meals'],
        'auth': res['result']['auth']
    }
    return render(request, 'home.html', context)

def meal(request, meal_id):
    req = urllib.request.Request('http://exp-api:8000/api/meal/' + str(meal_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    context = {
        'data': json.loads(resp_json)["result"]
    }
    return render(request, 'meal.html', context)

def createMeal(request):

    if not isAuth(request):
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'GET':
        return render(request, 'createmeal.html', {'form': forms.CreateMealForm()})

    form = forms.CreateMealForm(request.POST)

    if not form.is_valid():
        return render(request, 'createmeal.html')

    name = form.cleaned_data['name']
    price = form.cleaned_data['price']
    description = form.cleaned_data['description']
    portions = form.cleaned_data['portions']

    data_enc = urllib.parse.urlencode([('name', name), ('price', price), ('description', description), ('portions', portions)]).encode('utf-8')

    req = urllib.request.Request('http://exp-api:8000/api/createmeal/', data_enc)

    res = urllib.request.urlopen(req).read().decode('utf-8')

    resp = json.loads(res)

    if not resp or not resp['success']: # If login unsuccessful
        return render(request, 'createmeal.html', {'error': resp['result'] or "Could not create meal", 'form': forms.CreateMealForm()})

    return render(request, 'createmeal.html', {'created': True, 'form': forms.CreateMealForm()})

def isAuth(request):
    if not request.COOKIES.get('auth'):
        return False
    data_enc = urllib.parse.urlencode({'auth': request.COOKIES.get('auth')}).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/auth/', data_enc)
    res = urllib.request.urlopen(req).read().decode('utf-8')

    resp = json.loads(res)
    return resp['success']

def login(request):

    if request.method == 'GET':
        return render(request, 'login.html', {'form': forms.LoginForm()})

    form = forms.LoginForm(request.POST)

    if not form.is_valid():
        return render(request, 'login.html') # send an error if not valid

    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    data_enc = urllib.parse.urlencode([('email', email), ('password', password)]).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/login/', data_enc)

    res = urllib.request.urlopen(req).read().decode('utf-8')

    resp = json.loads(res)

    if not resp or not resp['success']: # If login unsuccessful
        return render(request, 'login.html', {'error': resp['result'] or "Error logging in", 'form': forms.LoginForm()})

    auth = resp['result']

    response = HttpResponseRedirect(reverse('home'))
    response.set_cookie("auth", auth)

    return response

def register(request):

    if request.method == 'GET':
        return render(request, 'register.html', {'form': forms.RegisterForm()})

    form = forms.RegisterForm(request.POST)

    if not form.is_valid():
        return render(request, 'register.html') # send an error if not valid

    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']

    data_enc = urllib.parse.urlencode([('email', email), ('password', password), ('first_name', first_name), ('last_name', last_name)]).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/register/', data_enc)

    res = urllib.request.urlopen(req).read().decode('utf-8')

    resp = json.loads(res)

    if not resp or not resp['success']: # If register unsuccessful
        return render(request, 'register.html', {'error': resp['result'] or "Error creating user", 'form': forms.RegisterForm()})

    # Created successfully, direct to login
    return HttpResponseRedirect(reverse('login'))

def logout(request):

    data_enc = urllib.parse.urlencode([('auth', request.COOKIES['auth'])]).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/logout/', data_enc)

    res = urllib.request.urlopen(req).read().decode('utf-8')

    resp = HttpResponseRedirect(reverse('home'))
    resp.delete_cookie('auth')

    return resp
