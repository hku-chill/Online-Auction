from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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