
from .basket import Basket

# run in every template


def basket(request):
    return {'basket': Basket(request)}
