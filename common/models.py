from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator

# ENUMS


GENDER = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    fullName = models.CharField(max_length=100,null=True,blank=True)
    gender = models.CharField(max_length=10,choices=GENDER,null=True,blank=True)    
    contactNumber = models.CharField(max_length=10,validators=[MinLengthValidator(10),MaxLengthValidator(10)],blank=True,null=True) 

class Invoice(models.Model):
    def CustomInvoiceId(self):
        return "INV" + str(self.id)
    order = models.CharField(max_length=20,blank=True,null=True)
    invoiceNo = property(CustomInvoiceId)
    invoiceDate=models.DateTimeField(auto_now_add = True)
