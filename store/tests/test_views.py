from unittest import skip  # allow test to skip  #python frame works

from django.contrib.auth.models import User
# test case is django standared libary,client is the function wich will go to browser and check if it works
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase  # django frame works
from django.urls import reverse

from store.models import Category, Product
from store.views import products_all  # homepage view


# skip is used to avoid any unwanted tests
@skip("demonstration")
class TestSkip(TestCase):
    def test_skip_example(self): pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()  # accessing requestfactory
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='100.00', image='django')

    def test_url_allowed_hosts(self):
        # test allowed hosts, domain
        response = self.c.get('/', HTTP_HOST='noaddress.com')  # self.c is the client
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        #  homepage response status
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):  # home page
        # code validation, search HTML for text
        request = HttpRequest()
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Bookstore</title>', html)
        self.assertEqual(response.status_code, 200)

    def test_homepage_factory(self):
        #  Using request factory
        request = self.factory.get('/django-beginners')
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Bookstore</title>', html)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):  # product
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))  # taking url
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):  # category
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)
