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


from django.http import response
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404

from .models import auction, category, bid

from .forms import BidForm

from user.helper import is_user_validated
from django.contrib.auth.decorators import login_required


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
        block_content = {
            'type': 'text',
            'value': auction_item.item_details
        }
        #auction body details
        if request.GET and request.GET.get("t"):
            if request.GET.get("t") == "bids":
                block_content = {
                    "type": "object_list",
                    "value_id": "bid_list",
                    "value": bid.objects.filter(auction=auction_item).order_by('-bid_date')
                }


        return render(request, 'auction/auction_item.html', {'auction_item': auction_item, 'highest_bid':highest, 'block_content': block_content })

#add bids to auction
def add_bid_to_auction(request, slug=None):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You need to authenticated to send bid to auction.", "footer": {"url": "/login/", "text": "Login Url"} })

    user_validate= is_user_validated(request.user)
    if not user_validate == True:
        if type(user_validate) == dict:
            return JsonResponse({"success": False, "message": user_validate['message'], "footer": {"url": user_validate['url'], "text": user_validate['url_text']} })

    
    #! check if auction slug came
    if not slug == None:

        #! check if auction exists
        auction_item = get_object_or_404(auction, slug=slug)

        """
        #! check if highest bid on auction exists
        #? Check if user has already bid on auction
        """
        try:
            highest_bid = bid.objects.get(auction=auction_item, is_bid_highest=True)
            is_user_has_bid = bid.objects.filter(auction=auction_item, user=request.user).exists()
        except bid.DoesNotExist:
            is_user_has_bid = False
            highest_bid = None

        #? if user already has bid on auction response Error
        #if not is_user_has_bid == False:
        #    return JsonResponse({"success": False, "message": "You have already bid on this auction, you can remove your bid and bid again on your profile.", "footer": {"url": "/profile/", "text": "Your Profile"} })

        #? Check if user request is GET thats mean he wants to see the form
        if request.method == 'GET' and request.GET.get('request_form') == 'true':
            bid_form = BidForm()
            return render(request, 'auction/add_bid.html', {'bid_form': bid_form, 'auction_item': auction_item, 'highest_bid':highest_bid})

        #? Check if user request is POST thats mean he wants to add bid
        elif request.method == 'POST' and request.POST.get('addBid_form') == 'true':
            bid_form = BidForm(request.POST)

            #? Check if form is valid
            if bid_form.is_valid():
                
                #!if user bid amouth is lower than initializing response error to user
                if auction_item.auction_initializing_bid >= int(bid_form.cleaned_data['bid_amount']):
                    return JsonResponse({"success": False, "message": "Your bid is lower than the auction's initializing bid."})

                #declare bid_obj veriable as bid model
                bid_obj = bid()
                bid_obj.auction = auction_item
                bid_obj.user = request.user
                bid_obj.bid_amount = bid_form.cleaned_data['bid_amount']
                bid_obj.save()
                
                response_data = {"success": True, "message": "Your bid successfuly added to auction..."}

            else:
                response_data = {"success": False, "message": "This bid is not valid please check again..."}

            return JsonResponse(response_data)
        else:
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")

