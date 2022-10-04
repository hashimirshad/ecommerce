from django.urls import path

from . import views

app_name ='store'
urlpatterns = [
    #home page
    path('',views.all_products, name='all_products'),
    #individual product details page first slug is data type and second is the value
    path('item/<slug:slug>/',views.product_detail,name='product_detail'),
    #individual cateogory details
    path('search/<slug:category_slug>/',views.category_list,name='category_list'),

]
