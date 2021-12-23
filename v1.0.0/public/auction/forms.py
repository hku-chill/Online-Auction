from django import forms
from django.contrib.auth.models import User
from .models import auction, bid, category, comment

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

class CreateAuctionForm(forms.ModelForm):
    TYPE_CHOICE = (
        ('hidden','hidden_bid'),
        ('shown', 'shown_bid'),
    )

    item_title = forms.CharField(
        label="Item name",
        help_text="Enter item name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter auction title.',
                'class': 'form-input border'
            }
        )
    )

    initializing_bid = forms.IntegerField(
        label="Initializing bid",
        help_text="Enter initializing bid",
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter initializing bid',
                'class': 'form-input border'
            }
        )
    )

    item_alt_title = forms.CharField(
        label="Item alt title",
        help_text="Enter item name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter item alt name.',
                'class': 'form-input border'
            }
        )
    )

    item_details = forms.CharField(
        label="Item details",
        help_text="Enter item details",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter item details',
                'class': 'form-input border'
            }
        )
    )
    item_condution = forms.CharField(
        label="Item condution",
        help_text="Enter item condution",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter item condution',
                'class': 'form-input border'
            }
        )
    )

    item_image = forms.ImageField(
        label="Item image",
        help_text="Enter item image",
        widget=forms.FileInput(
            attrs={
                'placeholder': 'Enter item image',
                'class': 'form-input border'
            }
        )
    )

    auction_end_date= forms.DateTimeField(
        label="Auction end date",
        help_text="Enter auction end date",
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': 'Enter auction end date',
                'class': 'form-input border',
                'type': 'date'
            }
        )
    )

    category = forms.CharField(
        label="Item category",
        help_text="Enter item category",
        widget=forms.HiddenInput(
            attrs={
                'placeholder': 'Enter item category',
                'class': 'form-input border'
            }
        )
    )

    auction_type = forms.ChoiceField(
        label="Auction type",
        help_text="Enter auction type",
        widget=forms.Select(
            attrs={
                'placeholder': 'Enter auction type',
                'class': 'form-input border'
            }
        ),
        choices=TYPE_CHOICE,
        initial='shown',
        required=True
    )

    class Meta:
        model = auction
        fields = ['item_title', 'item_alt_title', 'item_details', 'item_image', 'auction_type', 'initializing_bid', 'auction_end_date', 'item_condution']