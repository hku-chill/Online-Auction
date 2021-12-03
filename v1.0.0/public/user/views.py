from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import SignUpForm, LoginForm

from django.contrib import messages
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .helper import auth_user_should_not_access

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
        _profile = Profile.objects.get( pk=urlsafe_base64_decode(uid64) )
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