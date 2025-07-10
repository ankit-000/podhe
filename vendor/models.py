from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models.deletion import CASCADE, DO_NOTHING
from common.models import User

# ENUMS

STATES = (
    ("Andaman-and-Nicobar-Islands","Andaman and Nicobar Islands"),
    ("Andhra-Pradesh","Andhra Pradesh"),
    ("Arunachal-Pradesh","Arunachal Pradesh"),
    ("Assam","Assam"),
    ("Bihar","Bihar"),
    ("Chandigarh","Chandigarh"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Dadra-Nagar-Haveli","Dadra Nagar Haveli"),
    ("Delhi","Delhi"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal-Pradesh","Himachal Pradesh"),
    ("Jammu-and-Kashmir","Jammu and Kashmir"),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Ladakh","Ladakh"),
    ("Lakshadweep","Lakshadweep"),
    ("Madhya-Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Puducherry","Puducherry"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("TamilNadu","TamilNadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttarakhand","Uttarakhand"),
    ("Uttar-Pradesh","Uttar Pradesh"),
    ("West-Bengal","West Bengal"),
)

ACTYPE = (
    ("Current","Current"),
    ("Savings","Savings"),
)   


class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE,related_name="Vendor")
    companyName = models.CharField(max_length=100,default="",blank=True,null=True)    
    accountActive = models.BooleanField(default=False)
    panNumber = models.CharField(max_length=10,null=True,blank=True,validators=[MinLengthValidator(10),MaxLengthValidator(10)])
    gstNumber = models.CharField(max_length=15,null=True,blank=True,validators=[MinLengthValidator(15),MaxLengthValidator(15)])
    
    def __str__(self):
        return str(self.user)


class VendorBankDetails(models.Model):
    user = models.OneToOneField(Vendor,on_delete=CASCADE,related_name="bankDetails")
    bankName = models.CharField(max_length=100)
    IFSCCode = models.CharField(max_length=100)
    bankAccountNumber = models.CharField(max_length=100)
    accountName = models.CharField(max_length=100)
    accountType = models.CharField(choices=ACTYPE,blank=True,null=True,max_length=10)\
    
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Vendor Bank Details"

    
class VendorAddress(models.Model):
    user = models.OneToOneField(Vendor,on_delete=CASCADE,related_name="address")
    address1 = models.CharField(max_length=100,blank=True,null=True)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    landMark = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True,choices=STATES)
    pinCode = models.CharField(max_length=6,validators=[MinLengthValidator(6),MaxLengthValidator(6)])    

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Vendor Addresses"