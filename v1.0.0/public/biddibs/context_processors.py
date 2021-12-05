from auction.models import *


def category_context_processor(request):
    categories = category.objects.all()
    return {'categories_list': categories}