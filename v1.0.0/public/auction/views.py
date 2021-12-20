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


from django.shortcuts import HttpResponse, redirect, render, get_object_or_404

from .models import auction, category, bid

from .forms import BidForm, CommentForm


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
        return render(request, 'auction/auction_item.html', {'auction_item': auction_item})




#add bids to auction
def add_bid_to_auction(request, slug=None):
    if not slug == None:
        auction_item = get_object_or_404(auction, slug=slug)
        if request.method == 'POST':
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_obj = bid()
                bid_obj.auction = auction_item
                bid_obj.user = request.user
                bid_obj.bid_amount = bid_form.cleaned_data['bid_amount']
                bid_obj.save()

        else:
            bid_form = BidForm()
    
    return render(request, 'auction/add_bid.html', {'bid_form': bid_form, 'auction_item': auction_item})


def add_comment(request, slug=None):
    if not slug == None:
        auction_item = get_object_or_404(auction, slug=slug)
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.auction = auction_item
                comment.user = request.user
                comment.save()
                return redirect('auction:auction_item_url', slug=auction_item.slug)
        else:
            comment_form = CommentForm()
        return render(request, 'auction/add_comment.html', {'comment_form': comment_form})
   
  
