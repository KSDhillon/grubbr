from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from models import Order, User
import urllib.request
import urllib.parse
import json

    class UserTestCase(TestCase):
        #setUp method is called before each test in this class
        def setUp(self):
            pass #nothing to set up

        def create_user(self):
            user_data = {'email': 'dankramp@virginia.edu',
                         'password': 'password',
                         'first_name': 'Dan',
                         'last_name': 'Kramp'
            }
            
            post_encoded = urllib.parse.urlencode(user_data).encode('utf-8')

            req = urllib.request.Request('http://localhost:8000/api/user/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')

            self.assertContains(response, 'order_list')

        #user_id not given in url, so error
        def fails_invalid(self):
            response = self.client.get(reverse('all_orders_list'))
            self.assertEquals(response.status_code, 404)

        #tearDown method is called after each test
        def tearDown(self):
            pass #nothing to tear down
