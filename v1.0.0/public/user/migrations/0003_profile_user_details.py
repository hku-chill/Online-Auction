# Generated by Django 3.2.9 on 2021-12-18 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211212_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_details',
            field=models.CharField(blank=True, default='An awesome who want to be a BATMAN', max_length=255, null=True),
        ),
    ]
