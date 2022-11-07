import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings

from basket.basket import Basket
from orders.views import payment_confirmation

def order_placed(request):
    basket = Basket(request)
    basket.clear() # add function clear to basket/basket.py
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required #payment page
def BasketView(request):
    #basket is session make intent to sent to stripe
    basket = Basket(request) 
    total = str(basket.get_total_price())#sring
    total = total.replace('.', '') # what u mean by . for stripe integer only
    total = int(total) # integer totel
   #send stripe intent
   
    stripe.api_key =settings.STRIPE_SECRET_KEY #stripe api
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='inr',
        metadata={'userid': request.user.id} #maching up user with payment so we can use this data to retrive intant from strip for payment confirm
        
    )
    # rendering with user secret key with payment template,sending before payment page so we  can create user specific payment button
    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 
                                                            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})

@csrf_exempt
def stripe_webhook(request): #capture payment succeeded from strip and change billing status to true 
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key #stripe api
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded': #stripe event when successful
        payment_confirmation(event.data.object.client_secret) # finding order using client secret and orders.view

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

