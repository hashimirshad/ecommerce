from .models import Category


#user requst information
#category list for navigation bar dropdown
def categories(request):
    return{
        'categories':Category.objects.all()
    }
