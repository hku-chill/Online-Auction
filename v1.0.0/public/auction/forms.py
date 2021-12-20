from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import auction, bid, comment


class BidForm(forms.ModelForm):
    class Meta:
        model = bid
        fields = ['bid_amount']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='Message',
        
        widget=forms.Textarea(
            attrs={
                'placeholder': '  What is your view?',
                'class': 'form-input comment-name',
                'cols':70, 
                'rows':8, 
                     
            }
        
        
    ))
    class Meta:
        model = comment
        fields = ('name','body')

        
        