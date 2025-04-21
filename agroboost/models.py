from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLES = (
        ('SHG', 'Self Help Group'),
        ('FPG', 'Farmer Producer Group'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=USER_ROLES)

class Product(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)

class Resource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
