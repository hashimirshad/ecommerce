from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)  # basket session data available becuse of context_processor
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)

    # action='post',productid are collecting from jquery
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        # try:   we simply using shortcut method following code
        #   product = Product.objects.get(id=product_id)
        # except:
        #   raise http404
        basket.add(product=product, qty=product_qty)
        # we tead totel items in the cart
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty}) #the date rponse for rendering html
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid')) #user selected product id
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal}) #json responce send tohtml rendering
        return response


def basket_update(request):
    basket = Basket(request) #collecting data
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
