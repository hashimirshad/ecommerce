from .models import Category

# context processor allow site wide access
# user requst information
# category list for navigation bar dropdown


def categories(request):
    return {
        'categories': Category.objects.all()
    }
