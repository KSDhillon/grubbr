from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.request
import urllib.parse
from django.template import loader
import json
from . import forms

# Makes a request (POST if data is sent, GET else) and returns the response as a dict
def make_request(url, data={}):
    if data:
        enc_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, enc_data)
    else:
        req = urllib.request.Request(url)

    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(res_json)

def home(request):
    data = {}
    if request.COOKIES.get('auth'):
        data = {'auth': request.COOKIES.get('auth')}

    res = make_request('http://exp-api:8000/api/meals/', data)
    context = {
        'data': res['result']['meals'],
        'auth': res['result']['auth'],
        'cssfile': 'css/home.css',
    }
    return render(request, 'home.html', context)

def search_page(request):
    data = {}
    if request.COOKIES.get('auth'):
        data = {'auth': request.COOKIES.get('auth')}

    if request.method == 'GET':
        auth = isAuth(request)
        return render(request, 'search.html', { 'cssfile': 'css/search.css', 'form': forms.SearchForm(), 'auth': auth })

    form = forms.SearchForm(request.POST)

    if not form.is_valid():
        auth = isAuth(request)
        return render(request, 'search.html', { 'cssfile': 'css/search.css', 'form': forms.SearchForm(), 'auth': auth })

    q = form.cleaned_data['q']

    data['q'] = q
    res = make_request('http://exp-api:8000/api/search/', data)

    if not res or not res['success']: # If login unsuccessful
        return render(request, 'search.html', {'error': res['result'], 'form': forms.SearchForm(), 'cssfile': 'css/search.css'})

    return render(request, 'search.html', { 'cssfile': 'css/search.css', 'form': forms.SearchForm(), 'results': res['result']['results'], 'auth': res['result']['auth'] })

def meal(request, meal_id):
    data = {}
    if request.COOKIES.get('auth'):
        data = {'auth': request.COOKIES.get('auth')}

    res = make_request('http://exp-api:8000/api/meal/' + str(meal_id), data)
    context = {
        'data': res['result']['result'],
        'auth': res['result']['auth'],
        'cssfile': 'css/meal.css',
    }
    return render(request, 'meal.html', context)

def createMeal(request):

    if not isAuth(request):
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'GET':
        return render(request, 'createmeal.html', {'form': forms.CreateMealForm(), 'cssfile': 'css/createmeal.css', 'auth': True})

    form = forms.CreateMealForm(request.POST)

    if not form.is_valid():
        return render(request, 'createmeal.html', { 'cssfile': 'css/createmeal.css', 'auth': True })

    name = form.cleaned_data['name']
    price = form.cleaned_data['price']
    description = form.cleaned_data['description']
    portions = form.cleaned_data['portions']

    data = {'name': name,
            'price': price,
            'description': description,
            'portions': portions}
    res = make_request('http://exp-api:8000/api/createmeal/', data)

    if not res or not res['success']: # If login unsuccessful
        return render(request, 'createmeal.html', {'error': res['result'] or "Could not create meal", 'form': forms.CreateMealForm(), 'cssfile': 'css/createmeal.css', 'auth': True})

    return render(request, 'createmeal.html', {'created': True, 'form': forms.CreateMealForm(), 'cssfile': 'css/createmeal.css', 'auth': True})

def isAuth(request):
    if not request.COOKIES.get('auth'):
        return False
    data = {'auth': request.COOKIES.get('auth')}

    res = make_request('http://exp-api:8000/api/auth/', data)
    return res['success']

def login(request):

    if isAuth(request):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        return render(request, 'login.html', {'form': forms.LoginForm()})

    form = forms.LoginForm(request.POST)

    if not form.is_valid():
        return render(request, 'login.html', {'form': forms.LoginForm(), 'error': "Please enter a valid email."}) # send an error if not valid

    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    data = {'email': email, 'password': password}
    res = make_request('http://exp-api:8000/api/login/', data)

    if not res or not res['success']: # If login unsuccessful
        return render(request, 'login.html', {'error': res['result'] or "Error logging in", 'form': forms.LoginForm()})

    auth = res['result']

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

    data = {'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name}
    res = make_request('http://exp-api:8000/api/register/', data)

    if not res or not res['success']: # If register unsuccessful
        return render(request, 'register.html', {'error': res['result'] or "Error creating user", 'form': forms.RegisterForm()})

    # Created successfully, direct to login
    return HttpResponseRedirect(reverse('login'))

def logout(request):

    data = {'auth': request.COOKIES['auth']}
    res = make_request('http://exp-api:8000/api/logout/', data)

    resp = HttpResponseRedirect(reverse('home'))
    resp.delete_cookie('auth')

    return resp
