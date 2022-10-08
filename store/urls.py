from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    # home page
    path('', views.product_all, name='product_all'),
    # individual product details page first slug is data type and second is the value
    path('<slug:slug>', views.product_detail, name='product_detail'),
    # individual cateogory details
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),

]
