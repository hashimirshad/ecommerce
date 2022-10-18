import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
#from orders.views import payment_confirmation




@login_required #payment page
def BasketView(request):
    #basket is session make intent to sent to stripe
    basket = Basket(request) 
    total = str(basket.get_total_price())#sring
    total = total.replace('.', '') # what u mean by . for stripe integer only
    total = int(total) # integer totel
   #send stripe intent
   
    stripe.api_key = 'sk_test_51LrnhHSB7ADfnySMP7Ef2EbluaBBBnPeIWlEg2qT0PkRXSHtkktIj1x8EKswvnjede7jaRDb06lSozUn2KlLwhCT00N3nKSPrT' #stripe api
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='inr',
        metadata={'userid': request.user.id} #maching up user with payment so we can use this data to retrive intant from strip for payment confirm
        
    )
    # rendering with user secret key with payment template,sending before payment page so we  can create user specific payment button
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

