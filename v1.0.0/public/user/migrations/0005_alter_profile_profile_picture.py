# Generated by Django 3.2.9 on 2021-12-05 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/img/profile_pics/default.png', upload_to='static/img/profile_pics'),
        ),
    ]