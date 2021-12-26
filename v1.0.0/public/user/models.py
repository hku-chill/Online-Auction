from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.urls import reverse

import math
from auction.models import auction, bid, comment


class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='static/img/profile_pics', blank=True, default='static/img/profile_pics/default.png')

    address = models.CharField(max_length=255, null=True, blank=True)
    user_details = models.CharField(max_length=255, null=True, blank=True, default="An awesome user who want to be a BATMAN")

    user_rate_1 = models.IntegerField(default=0)
    user_rate_2 = models.IntegerField(default=0)
    user_rate_3 = models.IntegerField(default=0)
    user_rate_4 = models.IntegerField(default=0)
    user_rate_5 = models.IntegerField(default=1)

    tc = models.CharField(max_length=11, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    phone_verification_code = models.CharField(max_length=6, null=True, blank=True)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_tc_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def calc_rate_floor(self):
        if self.total_rate() == 0:
            return 0

        rate = (1*self.user_rate_1 + 2*self.user_rate_2 + 3*self.user_rate_3 + 4*self.user_rate_4 + 5*self.user_rate_5) / self.total_rate()

        return float(math.floor(rate))

    #return total bid of user
    def user_total_bid(self):
        return bid.objects.filter(user=self.user).count()

    #return total auction of user
    def user_total_auction(self):
        return auction.objects.filter(user=self.user).count()
    
    #return total comment of user
    def user_total_comment(self):
        return comment.objects.filter(user=self.user).count()

    def calc_rate_round(self):
        if self.total_rate() == 0:
            return 0
            
        rate = (1*self.user_rate_1 + 2*self.user_rate_2 + 3*self.user_rate_3 + 4*self.user_rate_4 + 5*self.user_rate_5) / self.total_rate()
        return float('{:.1f}'.format(rate))

    def total_rate(self):
        return self.user_rate_1 + self.user_rate_2 + self.user_rate_3 + self.user_rate_4 + self.user_rate_5

    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse("user:user_profile_url", kwargs={"userid": self.pk})
    
    def is_user_verified(self):
        return True
    

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

class Report(models.Model):
    REPORT_TYPE = (
        ('user', 'report_user'),
        ('auction', 'report_auction'),
        ('comment', 'report_comment'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    report_auction = models.ForeignKey(auction, on_delete=models.CASCADE, blank=True, null=True, related_name="report_auction")
    report_comment = models.ForeignKey(comment, on_delete=models.CASCADE, blank=True, null=True, related_name="report_comment")
    report_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="report_user")

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE, default="user")
    report_text = models.CharField(max_length=255, null=True, blank=True)
    report_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')












@receiver (post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile(user=instance).save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(pre_save, sender=Profile)
def delete_old_file(sender, instance, **kwargs):
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).profile_picture
    except sender.DoesNotExist:
        return False

    file = instance.profile_picture
    if not old_file == file:
        if old_file:
            old_file.delete(save=False)
        return False