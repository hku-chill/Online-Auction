from django.shortcuts import redirect, render, HttpResponse
from .models import category, auction

# Create your views here.
def index(request):
    return HttpResponse("selam_bebeq")

def get_auction_list(request):
    auction_list = auction.objects.all()
    return render(request, 'auction/auction_list.html', {'auction_list': auction_list})

def get_category_list(request):
    list_category = category.objects.all()
    if len(list_category) > 0:
        return render(request, 'auction/category_list.html', {'list_category': list_category})
    else:
        return redirect('/')
        


def get_category(request, slug=None):
    if not slug == None:
        try:
            category_item = category.objects.get(slug=slug)
            auction_list = auction.objects.filter(category=category_item)
            
            if len(auction_list) > 1:
                return render(request, 'auction/auction_list.html', {'auction_list': auction_list, 'category_item': category_item})
            else:
                return redirect('auction:category_index_url')

        except print(0):
            return redirect('/')
    else:
        return get_category_list(request)
