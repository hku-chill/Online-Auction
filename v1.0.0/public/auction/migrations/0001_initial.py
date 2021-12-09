# Generated by Django 3.2.9 on 2021-12-09 02:10

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
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Category')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(upload_to='static/img/category_imgs', verbose_name='Image')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Category Slug')),
                ('auction_count', models.PositiveIntegerField(default=0, verbose_name='Auction Count')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(max_length=100, verbose_name='Item Name')),
                ('item_alt_title', models.CharField(max_length=100, verbose_name='Item Alt Name')),
                ('item_image', models.ImageField(upload_to='static/img/auction_imgs', verbose_name='Item Image')),
                ('item_details', models.TextField(verbose_name='Item Details')),
                ('auction_slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Auction Slug')),
                ('auction_start_date', models.DateTimeField(auto_now_add=True, verbose_name='Auction Start Date')),
                ('auction_end_date', models.DateTimeField(verbose_name='Auction End Date')),
                ('auction_updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('auction_initializing_bid', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Auction Initializing Bid')),
                ('auction_is_active', models.BooleanField(default=True, verbose_name='Is Auction Active')),
                ('auction_type', models.CharField(choices=[('hidden', 'hidden_bid'), ('shown', 'shown_bid')], default='shown', max_length=10)),
                ('auction_rate_1', models.IntegerField(default=0)),
                ('auction_rate_2', models.IntegerField(default=0)),
                ('auction_rate_3', models.IntegerField(default=0)),
                ('auction_rate_4', models.IntegerField(default=0)),
                ('auction_rate_5', models.IntegerField(default=1)),
                ('auction_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL)),
                ('item_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='auction.category')),
            ],
            options={
                'verbose_name': 'Auction',
                'verbose_name_plural': 'Auctions',
                'ordering': ['-auction_start_date'],
            },
        ),
    ]
