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

    req = urllib.request.Request('http://models-api:8000/api/user/', signup_data)
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def logout(request):

    if request.method != "POST":
         return HttpResponse("Must be POST request")

    cook_dict = { 'auth': request.POST['auth'] }

    cookie =  urllib.parse.urlencode(cook_dict).encode('utf-8')

    req = urllib.request.Request('http://models-api:8000/api/logout/', cookie)
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
    if request.method != "POST":
        return HttpResponse("Must be POST request")

    meal_data =  urllib.parse.urlencode({"name": request.POST["name"], 
        "price": request.POST["price"],
        "description": request.POST["description"],
        "portions": request.POST["portions"],
        }).encode('utf-8')

    req = urllib.request.Request('http://models-api:8000/api/meal/', meal_data)
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def is_authenticated(request):
    auth = request.COOKIES.get['auth']
    authentication = urllib.parse.urlencode({"auth": request.POST['auth']})

    req = urllib.request.Request('http://models-api:8000/api/authenticate/', authentication)
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])
