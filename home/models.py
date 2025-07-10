from django.db import models

# Create your models here.

class RequestedProducts(models.Model):
    emailAddress = models.CharField(max_length=100,null=True,blank=True)
    fullName = models.CharField(max_length=100,null=True,blank=True)
    requestDescription = models.CharField(max_length=1000,null=True,blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)