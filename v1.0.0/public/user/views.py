# encoding:utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import *
from .helper import (auth_user_should_not_access, tc_user_should_not_access,
                     tcValidate)
from .models import Profile
from .token import account_activation_token


# Create your views here.
def user_logout(request):
    logout(request)
    return redirect('user:user_login_url')



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

            # Generate token for mail activation
            current_site = get_current_site(request)
            messages.add_message(request, messages.INFO, str("http://%s/activate/%s?token=%s" % (current_site.domain, urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(Profile.objects.get(user=user)) ) ) )

            # messages.add_message(request, messages.INFO, 'Registration is now complete, please check your mail address for activation.')
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
def mail_activate(request, uid64):
    try:
        _user = User.objects.get( pk=urlsafe_base64_decode(uid64) )
        _profile = _user.profile
    except Profile.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'User not found')
        return redirect('user:user_login_url')
    
    if not account_activation_token.check_token(_profile, request.GET.get('token')):
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




def user_profile(request, userid = None):
    return render(request, 'user/profile.html', {'profile': request.user.profile})

def user_profile_id(request, userid = None):
    return render(request, 'user/profile.html', {'profile': Profile.objects.get(pk=userid)})




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
