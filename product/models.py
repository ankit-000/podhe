from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.core.validators import MinLengthValidator
import itertools
from django.utils.text import slugify
from uuid import uuid4
from multiselectfield import MultiSelectField
from vendor.models import Vendor
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
import shutil
import os
from django_bleach.models import BleachField


OPTS = (
    ("Outdoor Plants","Outdoor Plants"),
    ("Office and desk Plants","Office and desk Plants"),
    ("Terrace Plants","Terrace Plants"),
    ("Balcony Plants","Balcony Plants"),
    ("Living Room Plants","Living Room Plants"),
    ("Bedroom Plants","Bedroom Plants"),
    ("Bathroom Plants","Bathroom Plants"),
    ("Kitchen Plants","Kitchen Plants"),
    ("Ac Room Plants","Table Top Plants"),
    ("Air purifying Plants","Air purifying Plants"),
    ("Winter Plant","Winter Plant"),
    ("Summer Plant","Summer Plant"),
    ("Monsoon Plant","Monsoon Plant"),
    ("All Season Plant","All Season Plant"),
    ("All Season Flower Plant","All Season Flower Plant"),    
)

SIZES = (
    ("Small","Small"),
    ("Medium","Medium"),
    ("Large","Large"),
    ("ExtraLarge","Extra Large"),
    ("NotApplicable","Not Applicable"),      
)

SEASONS = (
        ("Winter","Winter"),
        ("Summer","Summer"),
        ("Monsoon","Monsoon"),
        ("AllSeasons","All Seasons"),   
)

OCCASION = (
        ("NewYear","NewYear"),
        ("Holi","Holi"),
        ("WorldPlantDay","World Plant Day"),
        ("Rakhi","Rakhi"),
        ("OtherOccasions","Other Occasions"),
)

GIFTPACK = (
        ("Birthday","Birthday"),
        ("Anniversary","Anniversary"),
        ("Corporate","Corporate"),
        ("Other","Other"),
        ("NotApplicable","Not Applicable"),  
)

COMBOPACK = (      
        ("Buy1Get1 Free","Buy 1 Get 1 Free"),
        ("Buy2Get1Free","Buy 2 Get 1 Free"),
        ("Other","Other"),
        ("NotApplicable","Not Applicable"),
)

PRODUCTTYPE = (
    ("Product","Product"),
    ("Service","Service")
)

APPOINTMENTTIME = (
    ("09:00 AM - 12:00 PM","09:00AM-12:00PM"),
    ("12:00 PM - 03:00 PM","12:00PM-03:00PM"),
    ("03:00 PM - 06:00 PM","03:00PM-06:00PM"),
    ("06:00 PM - 09:00 PM","06:00PM-09:00PM"),
)

class Category(models.Model):
    categoryName = models.CharField(max_length=50, blank=True,null=True)
    categoryParentId = models.IntegerField(default=0)
    # categoryImage = models.ImageField()
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.categoryName

class Product(models.Model):        

    def _generate_slug(self):
        max_length = self._meta.get_field('sluggedName').max_length
        value = self.productName
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            c= Product.objects.filter(sluggedName=slug_candidate)                        
            if c.exists() and c[0].pk == self.pk:
                break
            elif not c.exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.sluggedName = slug_candidate

    def save(self, *args, **kwargs):
        #if not self.pk:
        self._generate_slug()
        super().save(*args, **kwargs)

    category = models.ForeignKey(Category,on_delete=CASCADE)
    tagCloud = MultiSelectField(choices=OPTS,default='')
    sluggedName = models.SlugField(default='',editable=False,max_length=500)    
    productName = models.CharField(max_length=100)
    productTable = BleachField()    
    productDescription = BleachField()    
    productMRP = models.FloatField()
    productSalePrice = models.FloatField()
    addedOn = models.DateTimeField(auto_now_add=True)
    uniqueId= models.UUIDField(default=uuid4, auto_created=True, editable=False, unique=True)
    addedBy = models.ForeignKey(Vendor,on_delete=CASCADE)
    size = models.CharField(max_length=100, blank=True,null=True,choices=SIZES)
    season = models.CharField(max_length=100, blank=True,null=True,choices=SEASONS)
    occasion = models.CharField(max_length=100, blank=True,null=True,choices=OCCASION)
    giftPack = models.CharField(max_length=100, blank=True,null=True,choices=GIFTPACK)
    comboPack = models.CharField(max_length=100, blank=True,null=True,choices=COMBOPACK)
    saleCounter = models.IntegerField(default=0)
    is_live = models.BooleanField(default=False)  
    taxPercent = models.FloatField()  
    totalUnitsSold = models.IntegerField(default=0,blank=True,null=True)
    unitsInStock = models.IntegerField(default=0,blank=True,null=True)
    is_visible = models.BooleanField(default=True)    
    appointmenttime =models.CharField(max_length=100,blank=True,null=True,choices=APPOINTMENTTIME)

    def __str__(self):
        return self.sluggedName


class ProductMedia(models.Model):

    def path_and_rename(instance, filename):  
        # instance.deleteimgkit()      
        ext = filename.split('.')[-1]        
        uploadpath =  "products/" + str(instance.product.sluggedName) + "/"             
        upload_to =   uploadpath        
        filename = '{}.{}'.format(instance.uniqueId, ext)             
        # return the whole path to the file
        return os.path.join(upload_to, filename)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    uniqueId= models.UUIDField(default=uuid4, auto_created=True, editable=False, unique=True)
    productmedia = models.FileField(blank=True,upload_to=path_and_rename)
    mainimage = models.BooleanField(default=False)

    def __str__(self):
        return str(self.productmedia)

    class Meta:
        verbose_name_plural = "Product Media"   

@receiver(pre_delete, sender=ProductMedia)
def delete_image(sender, instance, **kwargs):
# Pass false so FileField doesn't save the model.
    if instance.productmedia:
        kitlocation = os.path.join(settings.MEDIA_ROOT,"CACHE","images","products", str(instance.product.sluggedName + "\\"),str(instance.uniqueId))
        if os.path.exists(kitlocation):            
            if len(os.listdir(kitlocation))> 0:                
                    # os.remove(kitlocation)
                    shutil.rmtree(kitlocation)
        instance.productmedia.delete(False)


class ProductRating(models.Model):
    user = models.CharField(max_length=100,default="")
    rating = models.FloatField(default=0)
    addedOn = models.DateTimeField(auto_now_add=True)
    reviewSubject = models.CharField(max_length=200,default='',validators=[MinLengthValidator(10)])
    reviewDescription = models.TextField(max_length=1000, validators=[MinLengthValidator(50)])
    product = models.ForeignKey(Product,on_delete=DO_NOTHING)
    is_live = models.BooleanField(default=0)

    def __str__(self):
        return self.product.productName + " Rating"

class ProductRatingMedia(models.Model):

    def path_and_rename(instance, filename):  
        # instance.deleteimgkit()      
        ext = filename.split('.')[-1]        
        uploadpath =  "productreviews/" + str(instance.product.sluggedName) + "/" + instance.user + "/"             
        upload_to =   uploadpath        
        filename = '{}.{}'.format(instance.id, ext)             
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    user = models.CharField(max_length=100,default="")
    product = models.ForeignKey(Product,on_delete=DO_NOTHING)
    mediafile = models.FileField(blank=True,upload_to=path_and_rename)

    class Meta:
        verbose_name_plural = "Product Ratings Media"

    def __str__(self):
        return self.product.productName + "Rating Media"

class Coupon(models.Model):    
    couponCode = models.CharField(max_length=15,blank=True,null=True)
    validUpto = models.DateTimeField(null=True, blank=True)
    valueInPercent = models.FloatField(default=0.00)    
    currentRedemptions =models.IntegerField(blank=True,null=True,default=0)
    maxDiscount = models.FloatField(blank=True,null=True)
    maxRedemptions = models.IntegerField()

    class Meta:
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.couponCode
