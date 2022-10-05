# test case is django standared libary
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


# Category
class TestCategoriesModel(TestCase):

    def setUp(self):
        # created test data
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        # test functions so defined with starting "test_",insertion/types/fields attributes
        # self provide the defined above
        data = self.data1
        # self.assert do the testing
        self.assertTrue(isinstance(data, Category))
        # category model _str_ return name
        self.assertEqual(str(data), 'django')

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):

    def setUp(self):
        # foreignkey
        Category.objects.create(name='django', slug='django')
        # create user
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners',
                                            created_by_id=1, slug='django-beginners', price='100.00', image='django')
        # test data for product
        self.data2 = Product.products.create(category_id=1, title='django advanced', created_by_id=1,
                                             slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_product_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data1
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/django-beginners')
        response = self.client.post(
            reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        """
        Test product model custom manager returns only active products
        """
        data = Product.products.all()
        self.assertEqual(data.count(), 1)
