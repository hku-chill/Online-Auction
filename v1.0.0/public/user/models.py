from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")


    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
