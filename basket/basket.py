# model(functinalities) basket,functionality,call view
# Basket is called in context_processor so site wide update values,view only update views
from decimal import Decimal

from django.conf import settings

from store.models import Product


class Basket():
    # a base basket class ,providing some defualt behaviors that can be inherited or overrided , as necessary
    def __init__(self, request):
        # above self function can call any attribute within the function
        # initialise and run when created and available every page
        # building session, request.session wil look session data from http send by client
        self.session = request.session
        # session key available already
        basket = self.session.get('settings.BASKET_SESSION_ID')
        # if session not available create one
        if 'settings.BASKET_SESSION_ID' not in request.session:
            basket = self.session['settings.BASKET_SESSION_ID'] = {}
        self.basket = basket

    def add(self, product, qty):
        # adding and updating the users basket session data
        product_id = str(product.id)
        if product_id in self.basket:
            # if add same product again the qty replaced by new qty number else new creation
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products -itteration
        """
        # id:price,qty(1:150,2 ;2:200,4)these ids looped(assign) into a variable(product_id) using this variable we collecting the session data we need
        product_ids = self.basket.keys()
        # product manager sort is active, check product_id for session data
        products = Product.products.filter(id__in=product_ids)
        # copy session data
        basket = self.basket.copy()

        for product in products:
            # loop for collecting the product details like image
            basket[str(product.id)]['product'] = product

        # calculations
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        # __len__ will number of items in the list,python build in function
        # get basket data and count quantity of data
        # adding all the values
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty  # chang new qty value corresponding product id
        self.save()
    
    #cart totel price
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    #totel price with delivery
    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total

    def delete(self, product):
        """
        Delete item from session data ,
        """
        product_id = str(product)  # print(type(product_id))

        if product_id in self.basket:  # finding product in the basket
            del self.basket[product_id]
            # print(product_id) testing method for console
            self.save()
    def clear(self):
        # Remove basket from session
        del self.session['settings.BASKET_SESSION_ID'] #skey(settings.BASKET_SESSION_ID) intialized when created
        self.save()

    def save(self):  # modified self.save() call this function
        self.session.modified = True
