from django.shortcuts import render, HttpResponse
import urllib.request
import urllib.parse
from django.template import loader
import json

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
        return render(request, 'login.html')
    
    return HttpResponse(template.render(request))

def register(request):

    return render(request, 'register.html', context)
