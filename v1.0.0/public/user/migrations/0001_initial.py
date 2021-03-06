# Generated by Django 3.2.9 on 2021-12-22 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='static/img/profile_pics/default.png', upload_to='static/img/profile_pics')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('user_details', models.CharField(blank=True, default='An awesome who want to be a BATMAN', max_length=255, null=True)),
                ('user_rate_1', models.IntegerField(default=0)),
                ('user_rate_2', models.IntegerField(default=0)),
                ('user_rate_3', models.IntegerField(default=0)),
                ('user_rate_4', models.IntegerField(default=0)),
                ('user_rate_5', models.IntegerField(default=1)),
                ('tc', models.CharField(blank=True, max_length=11, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('phone_verification_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_tc_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
