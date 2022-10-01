from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)
    #define another names  
    class Meta:
        verbose_name_plural =  'categories'  
    def __str__(self):
        return self.name

class Product(models.Model):
    #on_delete=models.CASCADE will delete the product if catogory is deleted ,product is relation name
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    #delete if user deleted ,relation name
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_creator')
    title = models.CharField(max_length=255)
    #if no author defult name admin will given
    author = models.CharField(max_length=255 ,default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        #desending order last added will show first
        ordering = ('-created',)
    
    def __str__(self):
        return self.title

