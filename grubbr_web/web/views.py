from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, 'home.html')

def meal(request, meal_id):
    return render(request, 'meal.html')
