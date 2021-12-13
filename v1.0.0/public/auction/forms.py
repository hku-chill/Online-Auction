from django import forms
from django.contrib.auth.models import User
from .models import auction, bid


class BidForm(forms.ModelForm):
    class Meta:
        model = bid
        fields = ['bid_amount']