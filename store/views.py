from django.shortcuts import render,get_object_or_404, render

from .models import Category,Product


#user requst information
#category list for navigation bar dropdown
def categories(request):
    return{
        'categories':Category.objects.all()
    }

#product list
def all_products(request):
    products = Product.objects.all()
    #render load the data and html
    return render(request,'store/home.html',{'products':products})

#individual product details
def product_detail(request,slug):
    #select from the database where slug="value" eacch product have diffrent value
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request,'store/products/detail.html',{'product':product})

# category search
def category_list(request,category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    #proudt orm query
    products = Product.objects.filter(category=category)
    return render(request,'store/products/category.html', {'category': category, 'products': products})
    