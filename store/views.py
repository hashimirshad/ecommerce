from django.shortcuts import get_object_or_404, render

from .models import Category, Product


# product list
def product_all(request):
    # product manager is used to show only active objects turned in to product(second product it will search for the product manager)
    products = Product.products.all()
    #  render load the data and html
    return render(request, 'store/index.html', {'products': products})
# category search


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # proudt orm query
    products = Product.products.filter(category=category)  # product manager is used to show only active
    return render(request, 'store/category.html', {'category': category, 'products': products})

# individual product details


def product_detail(request, slug):
    # select from the database where slug="value" eacch product have diffrent value
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/single.html', {'product': product})
