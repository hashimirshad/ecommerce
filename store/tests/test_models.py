from django.test import TestCase
#test case is django standared libary
from django.contrib.auth.models import User

from store.models import Category, Product


#Category
class TestCategoriesModel(TestCase):
    def setUp(self):
        #created test data 
        self.data1 =Category.objects.create(name='django',slug='django')
    def test_category_model_entry(self):
        # test functions so defined with starting "test_",insertion/types/fields attributes
        #self provide the defined above
        data =  self.data1
        #self.assert do the testing
        self.assertTrue(isinstance(data,Category))

    def test_category_model_entry(self):
        #category model _str_ return name
        data =self.data1
        self.assertEqual(str(data),'django')
class TestProductsModel(TestCase):
    def setUp(self):
        #foreignkey
        Category.objects.create(name='django',slug='django')
        #create user
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1,title ='django beginners',created_by_id=1,slug='django-beginners',price='100.00',image='django')
    #test data for product
    def test_category_model_entry(self):
        data =self.data1
        self.assertTrue(isinstance(data,Product))
        self.assertEqual(str(data),'django beginners')

