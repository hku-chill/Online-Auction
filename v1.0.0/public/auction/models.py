from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from slugify import slugify

from django.urls import reverse
# Create your models here.

class auction(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='auctions')
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='auction/images/', verbose_name=_('Image'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('auction:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')
        ordering = ['-created_at']

class category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='static/img/category_imgs', verbose_name=_('Image'))
    slug = models.SlugField(unique=True, verbose_name=_('Category Slug'), blank=True)

    auction_count = models.PositiveIntegerField(default=0, verbose_name=_('Auction Count'))
    active_auction_count = models.PositiveIntegerField(default=0, verbose_name=_('Active Auction Count'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("auction:category_index_url", kwargs={"slug": self.slug})
    
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


@receiver(post_delete, sender=category)
def _post_delete_receiver(sender, instance, *args,  **kwargs):
    try:
        instance.image.delete(save=False)
    except print(0):
        pass

@receiver(post_save, sender=category)
def _post_save_receiver(sender, instance,created, *args,  **kwargs):
    if created:
        instance.slug = slugify(instance.name.lower())
        super(category, instance).save()



