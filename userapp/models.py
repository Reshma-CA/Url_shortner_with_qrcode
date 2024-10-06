from django.db import models
from . import utils

# Create your models here.

class People(models.Model):
    username = models.CharField(max_length=200,unique=True)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    confirm_password =models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Short_url(models.Model):
    user = models.ForeignKey(People, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True)
    short_url = models.URLField()
    qr_code_url = models.ImageField(upload_to='qr_codes/',blank=True, null=True)
    visit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.original_url} -> {self.short_url}'
    

    # class MyLink(models.Model):
#     source_link = models.URLField(max_length=300)
#     hash = models.CharField(max_length=50, default=utils.generate_hash, unique=True)
#     visit_count = models.IntegerField(default=0)  # To track number of visits
#     qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # To store QR code image
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.hash
    