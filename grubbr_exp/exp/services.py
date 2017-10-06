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
def get_meals(request):
    req = urllib.request.Request('http://models-api:8000/api/meal')
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])

def get_meal(request, meal_id):
    req = urllib.request.Request('http://models-api:8000/api/meal/' + str(meal_id))
    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    res = json.loads(res_json)
    return message(res["success"], res["result"])
