
from django.conf import settings #calling user model from settings used in created_by
from django.db import models
from django.urls import reverse  # tool alllow us to build url


# product manager to filter is active only show in the whole site using product manager filter out for any quary
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    # define another names

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        # store = app_name ,category_list=url name path (collecting url)
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    # on_delete=models.CASCADE will delete the product if catogory is deleted ,product is relation name
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    # delete if user deleted ,relation name
    #auth_user_model is calling from core/settings.py 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    # if no author defult name admin will given
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    # defult will allow image if creater deson't upload it
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'products'
        # desending order last added will show first
        ordering = ('-created',)
    # auto url for each product

    def get_absolute_url(self):
        # store = app_name ,product_detsil =url name path
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
