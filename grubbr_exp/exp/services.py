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
def recent_meals(request):
