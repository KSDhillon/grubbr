from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import json

def message(success, result):
    res = {
        'success': success,
        'result': result
    }
    return JsonResponse(res)

@csrf_exempt
def get_home_page(request):
    req = urllib.request.Request('http://models-api:8000/api/meal')
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def get_detail_page(request, meal_id):
    req = urllib.request.Request('http://models-api:8000/api/meal/' + str(meal_id))
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def create_account(request):
    if request.method != "POST":
        return HttpResponse("Must be POST request")

    signup_data =  urllib.parse.urlencode({"email": request.POST["email"], 
        "password": request.POST["password"],
        "first_name": request.POST["first_name"],
        "last_name": request.POST["last_name"],
        }).encode('utf-8')


    req = urllib.request.Request('http://models-api:8000/api/user/')
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def logout(request):
     if request.method != "POST":
         return HttpResponse("Must be POST request")

        
     req = urllib.request.Request('')
     res_json = urllib.request.urlopen(req).read().decode('utf-8')
     res = json.loads(res_json)
     return message(res["success"], res["result"])

def login(request):
    if request.method != "POST":
        return HttpResponse("Must be POST request")

    login_data =  urllib.parse.urlencode({"email": request.POST["email"], "password": request.POST["password"]}).encode('utf-8')

    req = urllib.request.Request('http://models-api:8000/api/login/', login_data)
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def create_new_listing(request):
    req = urllib.request.Request('')
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

