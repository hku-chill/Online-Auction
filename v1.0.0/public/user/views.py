# encoding:utf-8
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import *
from .helper import (auth_user_should_not_access, tc_user_should_not_access,
                     tcValidate, phoneValidate, is_user_validated)
from .models import Profile, Report
from .token import account_activation_token
from auction.models import auction, comment, bid
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Create your views here.
def user_logout(request):
    logout(request)
    return redirect('user:user_login_url')

from django.core.mail import EmailMessage

@auth_user_should_not_access
def register_user(request):

    msg = {
        'success': False,
        'message': '',
    }

    # Check if method is post
    if request.method == 'POST':
        # Change username field with email address
        request.POST = request.POST.copy()
        request.POST.update({
            "username":request.POST['email']
        })

        # save data as form data
        form = SignUpForm(request.POST)

        # check if form is valid
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_body = render_to_string('user/mailactivate.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(Profile.objects.get(user=user)),
            })

            email = EmailMessage(
                subject="Activate your account",
                body=mail_body,
                from_email="mahirtekin@indiryo.com",
                to=[user.email],
            )
            email.content_subtype = 'html'
            
            EmailThread(email).start()


            # Generate token for mail activation
            
            # messages.add_message(request, messages.INFO, str("http://%s/activate/%s?token=%s" % (current_site.domain, urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(Profile.objects.get(user=user)) ) ) )

            messages.add_message(request, messages.INFO, 'Registration is now complete, please check your mail address for activation.')
            return redirect('user:user_login_url')
        else:
            messages.add_message(request, messages.ERROR, 'Form is not valid')
    else:
        form = SignUpForm()

    return render(request, 'user/register.html', {'form': form, 'msg': msg})

@auth_user_should_not_access
def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        try:
            usr = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'There is not a user with this mail address..')
            form = LoginForm()
            return render(request, 'user/login.html', {'form': form})

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            if not form.get_user().is_active == True:
                messages.add_message(request, messages.ERROR, 'User is not active right now. Check your mail for activation.')
            else:
                login(request, form.get_user())
                return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, form.get_invalid_login_error())
    else:
        form = LoginForm()
    
    return render(request, 'user/login.html', {'form': form})

        # if user is not None:
        #     if user.is_active and user.profile.is_email_verified:
        #         login(request, user)
        #         return redirect('/')
        #     else:
        #         messages.add_message(request, messages.ERROR, 'Your account is not activated, please check your mail address for activation.')
        #         return redirect('user:user_login_url')
        # else:
        #     messages.add_message(request, messages.ERROR, 'Invalid username or password')

@auth_user_should_not_access
def mail_activate(request, uid64, token):
    print(token)
    try:
        _user = User.objects.get( pk=urlsafe_base64_decode(uid64) )
        _profile = _user.profile
    except Profile.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'User not found')
        return redirect('user:user_login_url')
    
    if not account_activation_token.check_token(_profile, token):
        messages.add_message(request, messages.ERROR, 'Invalid activation token or might be expired')
        return redirect('user:user_login_url')

    try:
        _profile.user.is_active = True
        _profile.user.save()
        _profile.is_email_verified = True
        _profile.save()
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('user:user_login_url')

    messages.add_message(request, messages.SUCCESS, "Your account is activated, please login")
    return redirect('user:user_login_url')

def edit_test(request):
    testform = AuthorUpdateView(None, instance=request.user.profile)
    return render(request, 'user/edittest.html', {'form': testform})


def user_profile(request, userid = None):
    # return render(request, 'user/profile.html', {'profile': request.user.profile})
    return user_profile_id(request, request.user.pk)

def user_profile_id(request, userid = None):
    r_user = get_object_or_404(User, pk=userid)
    block_content = {
        'object': None,
        'list': None,
        'type': 'text',
    }
    if request.GET.get('b'):
        block_content['object'] = request.GET.get('b')
        if block_content['object'] == "comments":
            block_content['list'] = comment.objects.filter(user=r_user)
        elif block_content['object'] == "bids":
            block_content['list'] = bid.objects.filter(user=r_user)
        else:
            block_content['list'] = auction.objects.filter(user=r_user)
    else:
        block_content['object'] = 'auctions'
        block_content['list'] = auction.objects.filter(user=r_user)

    if block_content['list'].count() > 0:
        block_content['type'] = 'list'
    else:
        block_content['type'] = 'text'
        block_content['list'] = f"There is no {block_content['object']} posted by this user"

    return render(request, 'user/profile.html', {'profile': r_user.profile, 'block_content': block_content})

def edit_profile(requst):
    return render(requst, 'user/editprofile.html')


@login_required(login_url='/login/')
@tc_user_should_not_access
def user_tc_validate_view(request):
    context = {'profile_form': TCForm_Profile(), 'user_form': TCForm_User()}
    return render(request, 'user/tcvalidate.html', context)

@login_required(login_url='/login/')
@tc_user_should_not_access
def user_tc_validate_end(request):
    if request.method == 'POST':
        profile_form = TCForm_Profile(request.POST)
        user_form = TCForm_User(request.POST)

        userr = User.objects.get(pk=request.user.pk)
        tc_filter = Profile.objects.filter(tc=request.POST['tc'])
        
        if tc_filter.exists() and not tc_filter[0] == userr.profile:
            return JsonResponse({'success': False, 'message': 'This TC number already used by other.'})
            

        if profile_form.is_valid() and user_form.is_valid():
            # user_form.save()
            userr.profile.tc = profile_form.cleaned_data['tc']
            userr.profile.birthday = profile_form.cleaned_data['birthday']
            userr.profile.is_tc_verified = True
            userr.profile.save()

            if tcValidate(request.POST.get('tc', ''), request.POST.get('first_name', ''), request.POST.get('last_name', ''), request.POST.get('birthday_year', '')):
                return JsonResponse({'success': True, 'message': 'TC validation success'})
            else:
                return JsonResponse({'success': False, 'message': 'TC validation failed'})
        
        return JsonResponse({'success': False, 'message': 'The informations not valid please check again...'})
    
    return HttpResponseBadRequest()


@login_required(login_url='/login/')
def user_mobile_validate_view(request):
    #check if user already verified his mobile
    if request.user.profile.is_phone_verified:
        return redirect('/')

    #create form veriables
    sms_form = None
    phone_form = None

    if request.method == 'POST':
        # check if this request came from first input type
        if request.POST.get('mobile_form_hidden') == 'True' :
            phone_form = MobileForm_Profile(request.POST)
            #? check if form is valid then send sms code to user and return sms validatation form
            if phone_form.is_valid():
                # send sms code to user
                validate_sms = phoneValidate(request.user, phone_form.cleaned_data['phone'])

                #if sms code sent to user render sms form
                if validate_sms:
                    phone_form = None
                    sms_form = SmsForm()

        # Check if this request came form code verification form
        elif request.POST.get('sms_form_hidden') == 'True':

            #! if somehow user's verification code got deleted from db then redirect to sms form
            if request.user.profile.phone_verification_code == None:
                sms_form = None
                phone_form = MobileForm_Profile()
            else:
                sms_form = SmsForm(request.POST)

                if sms_form.is_valid():
                    if request.user.profile.phone_verification_code == sms_form.cleaned_data['sms']:
                        request.user.profile.phone_verification_code = None
                        request.user.profile.is_phone_verified = True
                        request.user.profile.save(update_fields=['phone_verification_code', 'is_phone_verified'])
                        return redirect('/')
                    else:
                        sms_form.add_error('sms', 'SMS code is not valid, please check and try again.')
                        print(sms_form.errors)
    else:
        if request.user.profile.phone_verification_code:
            sms_form = SmsForm()
        else:
            phone_form = MobileForm_Profile()

    return render(request, 'user/mobilevalidate.html', {'mobile_form': phone_form, 'sms_form': sms_form})





def report_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You need to authenticated to send report something.", "footer": {"url": "/login/", "text": "Login Url"} })

    user_validate= is_user_validated(request.user)
    if not user_validate == True:
        if type(user_validate) == dict:
            return JsonResponse({"success": False, "message": user_validate['message'], "footer": {"url": user_validate['url'], "text": user_validate['url_text']} })

    if request.method == 'POST':
        report_obj = Report()
        report_obj.user = request.user

        #set report type
        report_obj.report_type = request.POST.get("input_type")

        if request.POST.get("input_type") == "auction":
            report_obj.report_auction = auction.objects.get(pk=request.POST.get("input_id"))
        elif request.POST.get("input_type") == "user":
            report_obj.report_user = get_user_model().objects.get(pk=request.POST.get("input_id"))
        elif request.POST.get("input_type") == "comment":
            report_obj.report_comment = comment.objects.get(pk=request.POST.get("input_id"))

        if request.POST.get("input_reason") == "":
            return JsonResponse({"success": False, "message": "Please select a reason for report."})

        else:
            report_obj.report_text = request.POST.get("input_reason")
            report_obj.save()

            response_data = {"success": True, "message": "Your report successfult send it..."}
    else:
        return HttpResponseBadRequest()



    return JsonResponse(response_data)