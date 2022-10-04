from unittest import skip
from urllib import response 
from django.test import TestCase,Client
#test case is django standared libary,client is the function wich will go to browser and check if it works 
from django.urls import reverse
from django.contrib.auth.models import User

from store.models import Category, Product

class TestViewResponses(TestCase):
    def  setUp(self):
        self.c = Client()
        User.objects.create(username='admin')
        Category.objects.create(name='django',slug='django')
        Product.objects.create(category_id=1,title ='django beginners',created_by_id=1,slug='django-beginners',price='100.00',image='django')
    def test_url_allowed_hosts(self):
        #test allowed hosts#homepage
        response = self.c.get('/')
        self.assertEqual(response.status_code,200)
    def test_product_detail_url(self):
        response =self.c.get(reverse('store:product_detail',args=['django-beginners']))
    def test_category_detail_url(self):
        response =self.c.get(reverse('store:category_list',args=['django']))

