from auction.models import *
from django.db.models import Count
from random import shuffle


def category_context_processor(request):
    categories = category.objects.annotate(num_books=Count('auctions')).order_by('-num_books')
    return {'categories_list': categories}

def auction_context_processor(request):
    auctions = auction.objects.all().order_by('-auction_start_date')
    return {'all_auction_list': auctions}