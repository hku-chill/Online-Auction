import datetime
import math

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class auction(models.Model):
    TYPE_CHOICE = (
        ('hidden','hidden_bid'),
        ('shown', 'shown_bid'),
    )
    
    # item details
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='auctions')
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Auction Slug'), blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='auctions')
    auction_is_active = models.BooleanField(default=True, verbose_name=_('Is Auction Active'))

    item_title = models.CharField(max_length=100, verbose_name=_('Item Name'))
    item_alt_title = models.CharField(max_length=100, verbose_name=_('Item Alt Name'))
    item_image = models.ImageField(upload_to='static/img/auction_imgs', verbose_name=_('Item Image'))
    item_details = models.TextField(verbose_name=_('Item Details'))
    item_condution = models.TextField(verbose_name=_('Item Condution Details'))




    # auction  details
    
    auction_start_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Auction Start Date'))
    auction_end_date = models.DateTimeField(verbose_name=_('Auction End Date'))
    auction_updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    auction_initializing_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Auction Initializing Bid'))

    # Auction system details
    
    auction_type = models.CharField(max_length=10 ,choices=TYPE_CHOICE, default='shown')

    auction_rate_1 = models.IntegerField(default=0)
    auction_rate_2 = models.IntegerField(default=0)
    auction_rate_3 = models.IntegerField(default=0)
    auction_rate_4 = models.IntegerField(default=0)
    auction_rate_5 = models.IntegerField(default=1)

    def __str__(self):
        return self.item_title

    def get_absolute_url(self):
        return reverse("auction:auction_item_url", kwargs={"slug": self.slug})

    def calc_rate_floor(self):
        if self.total_rate() == 0:
            return 0

        rate = (1*self.auction_rate_1 + 2*self.auction_rate_2 + 3*self.auction_rate_3 + 4*self.auction_rate_4 + 5*self.auction_rate_5) / self.total_rate()

        return float(math.floor(rate))
    
    def calc_rate_round(self):
        if self.total_rate() == 0:
            return 0
            
        rate = (1*self.auction_rate_1 + 2*self.auction_rate_2 + 3*self.auction_rate_3 + 4*self.auction_rate_4 + 5*self.auction_rate_5) / self.total_rate()
        return float('{:.1f}'.format(rate))

    def total_rate(self):
        return self.auction_rate_1 + self.auction_rate_2 + self.auction_rate_3 + self.auction_rate_4 + self.auction_rate_5

    class Meta:
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')
        ordering = ['-auction_start_date']

class category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='static/img/category_imgs', verbose_name=_('Image'))
    slug = models.SlugField(unique=True, verbose_name=_('Category Slug'), blank=True)

    auction_count = models.PositiveIntegerField(default=0, verbose_name=_('Auction Count'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("auction:category_item_url", kwargs={"slug": self.slug})
    
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class bid(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bids')
    auction = models.ForeignKey('auction', on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Bid Amount'))
    bid_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Bid Date'))
    is_bid_highest = models.BooleanField(default=False, verbose_name=_('Is Bid Highest'))

    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')
        ordering = ['-bid_amount']










from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from slugify import slugify

"""
    When a new category will created this function will be runned
    
    1- Create slug for category with using category name
"""
@receiver(post_save, sender=category)
def _category_create_receiver(sender, instance,created, *args,  **kwargs):
    if created:
        instance.slug = slugify(instance.name.lower())
        super(category, instance).save()


"""
    When a category is deleted, this function will be runned

    1- Delete category image from file system
"""
@receiver(post_delete, sender=category)
def _category_delete_receiver(sender, instance, *args,  **kwargs):
    try:
        instance.image.delete(save=False)
    except print(0):
        pass


"""
    When a auction created, this function will be runned

    1- Create slug for auction with using auction name
    2- Update category auction count
    3- Update category active auction count
"""
@receiver(post_save, sender=auction)
def _auction_create_receiver(sender, instance, created, *args,  **kwargs):
    if created:
        instance.slug = slugify(instance.item_title.lower())
        instance.category.auction_count = category.objects.filter(pk=instance.category.pk).count()
        super(auction, instance).save()
    
    """
        Update all categories by using auction list
    """
    cList = category.objects.all()
    for c in cList:
        c.auction_count = auction.objects.filter(category=c).count()
        c.save(update_fields=['auction_count'])

@receiver(pre_save, sender=auction)
def _auction_pre_save_receiver(sender, instance, *args,  **kwargs):
    try:
        old = auction.objects.get(pk=instance.pk)
    except auction.DoesNotExist:
        print("sa")
        return

"""
    When a auction deleted, this function will be runned

    1- Update category auction count
    2- Update category active auction count
    3- delte auction image from file system
"""
@receiver(post_delete, sender=auction)
def _auction_delete_receiver(sender, instance, *args,  **kwargs):
    instance.item_image.delete(save=False)



"""
    When a bid send to auction check if this bid is highest bid or not
"""
@receiver(pre_save, sender=bid)
def _bid_post_save_receiver(sender, instance, *args,  **kwargs):

    bids= bid.objects.filter(auction=instance.auction).order_by('-bid_amount')
    if bids.filter(is_bid_highest=True).exists():
        if bids.filter(is_bid_highest=True).count() > 1:
            bids.filter(is_bid_highest=True).update(is_bid_highest=False)
        
        bids.filter(pk=bids.filter(is_bid_highest=True).first().pk).update(is_bid_highest=True)

    else:
        bid.objects.filter(pk=bids[0].pk).update(is_bid_highest=True)
            
            
        

    return

@receiver(post_delete, sender=bid)
def _bid_post_delete_receiver(sender, instance, *args,  **kwargs):
    if instance.is_bid_highest == True:
        try:
            bids = bid.objects.filter(auction=instance.auction).order_by('-bid_amount')
            if bids.count() >= 1:
                bids[0].is_bid_highest = True
                print(bids[0].is_bid_highest)
                super(bid, bids[0]).save()
        except bid.DoesNotExist:
            pass
    

    



