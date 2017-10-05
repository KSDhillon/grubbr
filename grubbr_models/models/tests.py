from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import User
import urllib.request
import urllib.parse
import json

class UserTestCase(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.first_user = User.objects.create(email = "test@example.com", password = "password", first_name = "first", last_name = "user")
        
        sample_data = {'email': 'testp@virginia.edu',
                       'password': 'password',
                       'first_name': 'tester',
                       'last_name': 'testing'
        }
        
    def test_create_user(self):
        url = reverse('user_create')
        user_data = {'email': 'dankramp@virginia.edu',
                     'password': 'password',
                     'first_name': 'Dan',
                     'last_name': 'Kramp'
        }
        
        response = self.client.post(url, user_data, format='json')
        
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(pk=2)
        self.assertEqual(new_user.first_name, user_data['first_name'])
            
    def success_response(self):
        response = self.client.get(reverse('user_list', kwargs={'user_id':1}))
        self.assertContains(response, 'user_list')   
            
            
    def update_info(self):
        url = reverse('user_info', args=[self.first_user.id])
            
        response = self.client.put(url, self.sample_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
            
    def delete_user(self):
        url = reverse('user_info', args=[self.first_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            
    def fails_invalid(self):
        response = self.client.get(reverse('user_list'))
        self.assertEquals(response.status_code, 404)
              
    def tearDown(self):
        pass
        

    
