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
    context = {
        'data': json.loads(resp_json)["result"]
    }
    return render(request, 'home.html', context)

def meal(request, meal_id):
    req = urllib.request.Request('http://exp-api:8000/api/meal/' + str(meal_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    context = {
        'data': json.loads(resp_json)["result"]
    }
    return render(request, 'meal.html', context)

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
#    return render(request, 'login.html', {'success': 'Account created successfully! Login below:'})
