"""
 █████   █████ █████  █████ ██████   ██████ ███████████  █████       ██████████   █████  █████ ██████   ██████ ███████████ 
░░███   ░░███ ░░███  ░░███ ░░██████ ██████ ░░███░░░░░███░░███       ░░███░░░░███ ░░███  ░░███ ░░██████ ██████ ░░███░░░░░███
 ░███    ░███  ░███   ░███  ░███░█████░███  ░███    ░███ ░███        ░███   ░░███ ░███   ░███  ░███░█████░███  ░███    ░███
 ░███████████  ░███   ░███  ░███░░███ ░███  ░██████████  ░███        ░███    ░███ ░███   ░███  ░███░░███ ░███  ░██████████ 
 ░███░░░░░███  ░███   ░███  ░███ ░░░  ░███  ░███░░░░░███ ░███        ░███    ░███ ░███   ░███  ░███ ░░░  ░███  ░███░░░░░░  
 ░███    ░███  ░███   ░███  ░███      ░███  ░███    ░███ ░███      █ ░███    ███  ░███   ░███  ░███      ░███  ░███        
 █████   █████ ░░████████   █████     █████ ███████████  ███████████ ██████████   ░░████████   █████     █████ █████       
░░░░░   ░░░░░   ░░░░░░░░   ░░░░░     ░░░░░ ░░░░░░░░░░░  ░░░░░░░░░░░ ░░░░░░░░░░     ░░░░░░░░   ░░░░░     ░░░░░ ░░░░░        
                                                                                                                           
                                                                                                                           
                                                                                                                           
"""


from django.http.response import HttpResponseBadRequest
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404

from .models import auction, category, bid

from .forms import BidForm


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
            
            if len(auction_list) > 0:
                return render(request, 'auction/auction_list.html', {'auction_list': auction_list, 'category_item': category_item})
            else:
                return redirect('auction:category_index_url')

        except print(0):
            return redirect('/')
    else:
        return get_category_list(request)


def get_auction(request, slug=None):
    if not slug == None:
        auction_item = auction.objects.get(slug=slug)

        try:
            highest = bid.objects.get(auction=auction_item, is_bid_highest=True)
        except bid.DoesNotExist:
            highest = None
            pass

        return render(request, 'auction/auction_item.html', {'auction_item': auction_item, 'highest_bid':highest})

#add bids to auction
def add_bid_to_auction(request, slug=None):
    if not slug == None:
        auction_item = get_object_or_404(auction, slug=slug)

        try:
            highest_bid = bid.objects.get(auction=auction_item, is_bid_highest=True)
        except bid.DoesNotExist:
            highest_bid = None


        if request.method == 'GET' and request.GET.get('request_form') == 'true':
            bid_form = BidForm()
            return render(request, 'auction/add_bid.html', {'bid_form': bid_form, 'auction_item': auction_item, 'highest_bid':highest_bid})
        elif request.method == 'POST' and request.POST.get('addBid_form') == 'true':
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_obj = bid()
                bid_obj.auction = auction_item
                bid_obj.user = request.user
                bid_obj.bid_amount = bid_form.cleaned_data['bid_amount']
                bid_obj.save()
                return HttpResponse("bid added")
            else:
                return render(request, 'auction/add_bid.html', {'bid_form': bid_form, 'auction_item': auction_item, 'highest_bid':highest_bid})
            
            

    return HttpResponseBadRequest("Slug not found")
    if not slug == None:
        auction_item = get_object_or_404(auction, slug=slug)

        try:
            highest_bid = bid.objects.get(auction=auction_item, is_bid_highest=True)
        except bid.DoesNotExist:
            highest_bid = None

        if request.method == 'POST':
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_obj = bid()
                bid_obj.auction = auction_item
                bid_obj.user = request.user
                bid_obj.bid_amount = bid_form.cleaned_data['bid_amount']
                bid_obj.save()
                return redirect('auction:auction_item_url', slug=slug)

        else:
            bid_form = BidForm()
    
    return render(request, 'auction/add_bid.html', {'bid_form': bid_form, 'auction_item': auction_item, 'highest_bid':highest_bid})
