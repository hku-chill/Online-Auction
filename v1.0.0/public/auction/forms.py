from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import auction, bid, comment, report


class BidForm(forms.ModelForm):
    class Meta:
        model = bid
        fields = ['bid_amount']

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        
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
        fields = ['body']


class ReportForm(forms.ModelForm):
    text=forms.Charfield()

    class Meta:
        model = report
        fields = ['text']

    

        
        