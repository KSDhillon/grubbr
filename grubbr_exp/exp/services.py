from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import json

def message(success, result):
    res = {
        'success': success,
        'result': result
    }
    return JsonResponse(res)

# Makes a request (POST if data is sent, GET else) and returns the response as a dict
def make_request(url, data={}):
    if data:
        enc_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, enc_data)
    else:
        req = urllib.request.Request(url)

    res_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(res_json)

def get_home_page(request):

    res = make_request('http://models-api:8000/api/meal')

    return message(res["success"], {'meals': res["result"], 'auth': check_auth(request)})

def get_detail_page(request, meal_id):
    res = make_request('http://models-api:8000/api/meal/' + str(meal_id))
    return message(res["success"], res["result"])

def create_account(request):
    if request.method != "POST":
        return HttpResponse("Must be POST request")

    signup_data = {"email": request.POST["email"],
        "password": request.POST["password"],
        "first_name": request.POST["first_name"],
        "last_name": request.POST["last_name"],
    }
    res = make_request('http://models-api:8000/api/user/', signup_data)
    return message(res["success"], res["result"])


def logout(request):

    if request.method != "POST":
         return HttpResponse("Must be POST request")

    cookie = { 'auth': request.POST['auth'] }
    res = make_request('http://models-api:8000/api/logout/', cookie)
    return message(res["success"], res["result"])

def login(request):
    if request.method != "POST":
        return HttpResponse("Must be POST request")

    login_data = {"email": request.POST["email"], "password": request.POST["password"]}
    res = make_request('http://models-api:8000/api/login/', login_data)
    return message(res["success"], res["result"])


def create_new_listing(request):

    if request.method != "POST":
        return message(False, "Must be POST request")

    if (not request.POST['name'] or
        not request.POST['price'] or
        not request.POST['description'] or
        not request.POST['portions']):
        return message(False, "Not all required fields provided.")

    meal_data =  {"name": request.POST["name"],
        "price": request.POST["price"],
        "description": request.POST["description"],
        "portions": request.POST["portions"],
    }

    res = make_request('http://models-api:8000/api/meal/', meal_data)
    if res['success']: # Send to Kafka queue
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('new-listings-topic', json.dumps(res['result']).encode('utf-8'))
    return message(res["success"], res["result"])

def is_authenticated(request):

    return message(check_auth(request), "auth status")

def check_auth(request):
    if request.method == 'POST' and request.POST['auth']:
        authentication = {"auth": request.POST['auth']}

        res = make_request('http://models-api:8000/api/authenticate/', authentication)
        return res['success']
    return False

def search_listings(request):
    if not request.POST['q']: # Query is passed in as GET data 'q'
        return message(False, 'No query provided')

    es = Elasticsearch(['es'])
    res = es.search(index='listing_index', body={'query': {'query_string': {'query': request.POST['q']}}, 'size': 10})

    results = []
    if not res['timed_out']:
        for r in res['hits']['hits']:
            results.append(r['_source'])

    return message(True, {'results': results, 'auth': check_auth(request)})
