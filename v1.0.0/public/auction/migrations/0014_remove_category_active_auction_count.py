# Generated by Django 3.2.9 on 2021-12-07 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_auto_20211207_0330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='active_auction_count',
        ),
    ]
