from auction.models import *
from random import shuffle


def category_context_processor(request):
    categories = category.objects.all()
    return {'categories_list': categories}