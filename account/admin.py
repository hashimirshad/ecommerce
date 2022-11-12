from django.contrib import admin

from .models import Customer

# admin login page
admin.site.register(Customer)
