from decimal import Decimal
from django.conf import settings # (foreign key ACCESS) to access user information we declared custom user model in setting
from django.db import models

from store.models import Product


class Order(models.Model):
    #data is collecting from setting/custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    #order key is assosiated with client secret so we can confirm the payment from the stripe using this data
    order_key = models.CharField(max_length=200)#unique  key
    billing_status = models.BooleanField(default=False) # defult false data collected from stripe and it willl change to true


    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)

# each order may have many item one to many 
class OrderItem(models.Model):
    #collecting data to show ordered product becuse price will change in product table so we want to store purchased price
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2) #to store purchased price & quantity
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
