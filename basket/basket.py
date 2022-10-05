# model(functinalities) basket,functionality,call view
from decimal import Decimal

from store.models import Product


class Basket():
    # a base basket class ,providing some defualt behaviors that can be inherited or overrided , as necessary
    def __init__(self, request):
        # above self function can call any attribute within the function
        # initialise and run when created and available every page
        # building session, request.session wil look session data from http send by client
        self.session = request.session
        # session key available already
        basket = self.session.get('skey')
        # if session not available create one
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        # adding and updating the users basket session data
        product_id = str(product.id)
        if product_id in self.basket:
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
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_total_price(self):
        # summing up the values of the cart
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    def save(self):
        self.session.modified = True
