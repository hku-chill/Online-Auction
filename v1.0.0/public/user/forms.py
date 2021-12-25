from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import generic

from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, required=True, label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    username = forms.CharField(
        max_length=30, required=True, label='Username',
        widget=forms.HiddenInput()
    )

    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}
        )
    )

    password1 = forms.CharField(
        widget= forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )

    password2 = forms.CharField(
        widget= forms.PasswordInput(
            attrs={'placeholder': 'Password Again'}
        )
    )

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password1', 'password2', 'username')

class AuthorUpdateView(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthday', 'phone','profile_picture', 'tc')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30, required=True, label='email',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address.'})
    )

    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )


    class Meta:
        model = User
        fields = ('username', 'password')

class TCForm_User(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30, required=True, label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name.'})
    )
    last_name = forms.CharField(
        max_length=30, required=True, label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Last name.'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class TCForm_Profile(forms.ModelForm):
    tc = forms.CharField(
        label='TC Number',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter your TC number',
                'class': 'form-input'
            }
        )
    )


    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1930, 2012),attrs={'class': 'form-select'}))
    class Meta:
        model = Profile
        fields = ('tc', 'birthday')

class SmsForm(forms.Form):
    sms_form_hidden = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={'value': 'True'}
        )
    )

    sms = forms.CharField(
        label='SMS Code',
        help_text='Enter the code sent to your phone.',
        min_length=6,
        max_length=6,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter the code',
                'class': 'form-input'
            }
        )
    )
    class Meta:
        model = Profile
        fields = ('sms','sms_form_hidden')

class MobileForm_Profile(forms.ModelForm):
    mobile_form_hidden = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={'value': 'True'}
        )
    )
    phone = forms.CharField(
        label="Mobile Number",
        help_text= "Enter your mobile number eg. 5528842333",
        min_length=10,
        max_length=10,
        widget= forms.NumberInput(
            attrs={
                'placeholder': '5xxxxxxxxx',
                'class': 'form-input'
            }
        )
    )
    class Meta:
        model = Profile
        fields = ('phone', 'mobile_form_hidden')