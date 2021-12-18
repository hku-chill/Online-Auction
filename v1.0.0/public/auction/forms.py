from django import forms
from django.contrib.auth.models import User
from .models import auction, bid


class BidForm(forms.ModelForm):
    bid_amount = forms.CharField(
        label="Bid amouth",
        help_text="Enter bid amouth",
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter bid amouth',
                'class': 'form-input border'
            }
        )
    )

    class Meta:
        model = bid
        fields = ['bid_amount']
