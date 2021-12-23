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

from .models import auction, category, bid, comment,rates

from .forms import BidForm, CreateAuctionForm, CommentForm

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
                bid_list = bid.objects.filter(auction=auction_item).order_by('-bid_date')
                block_content = {
                    "type": "object_list" if bid_list.count() > 0 else "text",
                    "value_id": "bid_list",
                    "value": bid_list if bid_list.count() > 0 else "There is no bid right now. Do you want to be first?"
                }
            elif request.GET.get("t") == "comments":
                block_content= {
                    "type": "object_list",
                    "value_id": "comment_list",
                    "value": comment.objects.filter(auction=auction_item).order_by('-created')
                }


        return render(request, 'auction/auction_item.html', {'auction_item': auction_item, 'highest_bid':highest, 'block_content': block_content })


#create new auction view
@login_required(login_url='/login/')
def create_auction(request):
    
    user_validate= is_user_validated(request.user)
    if not user_validate == True:
        if type(user_validate) == dict:
            return redirect(user_validate['url'])

    if request.method == 'POST':
        form = CreateAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            new_auction = auction()

            new_auction.item_title = form.cleaned_data['item_title']

            new_auction.item_alt_title = form.cleaned_data['item_alt_title']

            new_auction.auction_initializing_bid = form.cleaned_data['initializing_bid']

            new_auction.item_details = form.cleaned_data['item_details']
            new_auction.item_condution = form.cleaned_data['item_condution']

            new_auction.item_image = form.cleaned_data['item_image']
            new_auction.auction_end_date = form.cleaned_data['auction_end_date']

            new_auction.category = category.objects.get(slug=form.cleaned_data['category'])
            new_auction.user = request.user

            new_auction.save()
            
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'auction/create_auction.html', {'form': form})
    else:
        form = CreateAuctionForm()

    return render(request, 'auction/create_auction.html', {'form': form})

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
        
        if auction_item.user == request.user:
            return JsonResponse({"success": False, "message": "You can not bid on your own auction."})

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
        if not is_user_has_bid == False:
           return JsonResponse({"success": False, "message": "You have already bid on this auction, you can remove your bid and bid again on your profile.", "footer": {"url": "/profile/", "text": "Your Profile"} })

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


@login_required(login_url='/login/')
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




def rate_auction(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You need to authenticated to send rate auctions.", "footer": {"url": "/login/", "text": "Login Url"} })

    user_validate= is_user_validated(request.user)
    if not user_validate == True:
        if type(user_validate) == dict:
            return JsonResponse({"success": False, "message": user_validate['message'], "footer": {"url": user_validate['url'], "text": user_validate['url_text']} })

    if request.method == "GET" and request.GET.get("rate") and request.GET.get('auction-slug'):
        auct = get_object_or_404(auction, slug=request.GET.get('auction-slug'))

        #take requested rate number
        requested_rate = getattr(auct, 'auction_rate_'+request.GET.get("rate"))

        #check if user has already rated auction
        if rates.objects.filter(user=request.user, auction=auct).exists():
            old_rate = rates.objects.get(user=request.user, auction=auct)
            

            if old_rate.rate == int(request.GET.get("rate")):
                return JsonResponse({"success": False, "message": f"You have already rated this auction with {old_rate.rate}."})
            else:
                #change old rate
                old_requested_rate = getattr(auct, f'auction_rate_{old_rate.rate}')
                old_requested_rate -= 1
                setattr(auct, f'auction_rate_{old_rate.rate}', old_requested_rate)

                #change new rate
                requested_rate += 1
                setattr(auct, 'auction_rate_'+request.GET.get('rate'), requested_rate)
                auct.save()

                #change rate object to new rate
                old_rate.rate = request.GET.get("rate")
                old_rate.save()
                return JsonResponse({"success": True, "message": f"Your rate changed to {request.GET.get('rate')}."})
        else:
            requested_rate += 1
            setattr(auct, 'auction_rate_'+request.GET.get('rate'), requested_rate)
            auct.save()

            #create new rate object
            rate_obj = rates()
            rate_obj.user = request.user
            rate_obj.auction = auct
            rate_obj.rate = request.GET.get('rate')
            rate_obj.save()
            return JsonResponse({"success": True, "message": f"Your rate added to {request.GET.get('rate')}."})
    else:
        return HttpResponseBadRequest("Bad Request")