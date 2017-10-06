from django.shortcuts import render, HttpResponse
import urllib.request
import urllib.parse
from django.template import loader
import json

def home(request):
    template = loader.get_template('home.html')
    req = urllib.request.Request('http://exp-api:8000/api/meals')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    context = {
        'data': json.loads(resp_json)["result"]
    }
    return HttpResponse(template.render(context, request))

def meal(request, meal_id):
    template = loader.get_template('meal.html')
    req = urllib.request.Request('http://exp-api:8000/api/meal/' + str(meal_id))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    context = {
        'data': json.loads(resp_json)["result"]
    }
    return HttpResponse(template.render(context, request))
