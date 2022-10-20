from django.http.response import JsonResponse #to send json using capturing ajax
from django.shortcuts import render

from basket.basket import Basket # we are using session data

from .models import Order, OrderItem #tables required


def add(request): 
    basket = Basket(request)
    if request.POST.get('action') == 'post': #cross checking with ajax using action name basket is called perfectly

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists(): #aviod repeatation it will show in admin add admin.py
            pass
        else: # collecting data from user table and basket and creating order and order item
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True) # orderkey equal to intent data
    


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders