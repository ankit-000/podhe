from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.core.validators import MaxLengthValidator, MinLengthValidator
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

ORDERSTATUS = (
    ("PaymentPending","Payment Pending"),    
    ("Cancelled","Cancelled"),
    ("RefundPending","Refund Pending"),
    ("Processing","Processing"),
    ("Packed","Packed"),
    ("Shipped","Shipped"),
    ("Delivered","Delivered"),
    ("ReturnRequested","Return Requested"),
    ("RefundIssued","Refund Issued"),
)

COURIERPARTNERS = (
    ('DelhiVery','Delivery'),
    ('BlueDart','BlueDart'),
    ('DHL','DHL'),
    ('Ekart','Ekart'),
    ('DTDC','Podhewale'),
    ('Aramex','Aramex'),
    ('Ecom','Ecom'),
    ('FedEx','FedEx'),
    ('Gati','Gati'),
    ('SafeExpress','SafeExpress'),
    ('ProfessionalCouriers','ProfessionalCouriers'),

)

# ADDRESSTYPE = (
#     ('Billing Address','BillingAddress'),
#     ('Shipping Address','ShippingAddress'),    

# )


# OTPType = (
#     ("SignUp","SignUp"),
#     ("PasswordReset","PasswordReset"),
# )

# class UserOTP(models.Model):
#     user = models.OneToOneField(User,on_delete=CASCADE)
#     otp = models.CharField(max_length=6,null=True,blank=True)
#     active =models.BooleanField(default=False)
#     lastgeneratedon = models.DateTimeField(blank=True,null=True)
#     lastusedon = models.DateTimeField(blank=True,null=True)
#     usedfor = models.CharField(choices=OTPType, max_length=50)

#     class Meta:
#         verbose_name_plural = "User OTP"


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE,related_name="Customer")
    # otpType = models.CharField(max_length=100,choices=OTPType, default=None)
    otpNumber = models.TextField(max_length=6,default=0,blank=True)

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user = models.ForeignKey(Customer,on_delete=CASCADE,related_name="address")
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city= models.CharField(max_length=100,blank=True,null=True)
    landMark = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,choices=STATES,default=None)
    pinCode = models.CharField(max_length=6,validators=[MinLengthValidator(6),MaxLengthValidator(6)])
    contactNumber = models.CharField(max_length=10,validators=[MinLengthValidator(10),MaxLengthValidator(10)])
    contactPerson = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=0)
    is_active = models.BooleanField(default=1)
    # address_type=models.CharField(max_length=100,choices=ADDRESSTYPE,default=None)

    def __str__(self):
        return str(self.user.user)

class Order(models.Model):
    def CustomOrderId(self):
        return "ORD" + self.orderedOn.strftime("%m%d%Y") + str(self.id)
    
    user = models.ForeignKey(User,on_delete=DO_NOTHING)    
    orderId= property(CustomOrderId)
    orderedOn = models.DateTimeField(auto_now_add=True)
    couponCode = models.CharField(max_length=100,blank=True,null=True)
    discount = models.FloatField(blank=True, null=True,default=0)
    orderTotal = models.FloatField(blank=True, null=True,default=0)
    taxOnOrder = models.FloatField(blank=True, null=True,default=0)
    orderStatus = models.CharField(max_length=100,choices=ORDERSTATUS)
    razorOrderId = models.CharField(max_length=50,blank=True,null=True)
    razorPaymentId = models.CharField(max_length=50,blank=True,null=True)
    razorSignature = models.CharField(max_length=150,blank=True,null=True)
    trackingInfo = models.CharField(max_length=30,blank=True,null=True,default='')
    trackingProvider = models.CharField(max_length=100,choices=COURIERPARTNERS,null=True,blank=True,default='')
    addressid = models.IntegerField()
    deliveryDate = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.orderId

    class Meta:
        verbose_name_plural = "Orders"

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=CASCADE)
    productId = models.CharField(max_length=100)
    productName = models.CharField(max_length=200)
    unitPrice = models.FloatField(default=0)
    listPrice = models.FloatField(default=0)
    paidPrice = models.FloatField(default=0)
    taxAmount = models.FloatField(default=0)
    discountAmount = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    vendorId = models.IntegerField()
    userId = models.CharField(max_length=100, default='')    
    returnRequested = models.BooleanField(default=0)
    returnStatus = models.CharField(max_length=50,blank=True,null=True)
    appointmentDate = models.CharField(max_length=100)
    appointmentTime = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Order Items"

    def __str__(self):
        return str(self.order.orderId) + "  Product Name: " + str(self.productName) + " Quantity: " + str(self.quantity)

class RazorOrder(models.Model):
    razorOrderId = models.CharField(max_length=50,blank=True,null=True)
    userId = models.CharField(max_length=50,blank=True,null=True)
    cartDict = models.CharField(max_length=500,blank=True,null=True)
    checkoutTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razorOrderId


class WishList(models.Model):
    user=models.ForeignKey(Customer,on_delete=CASCADE)
    productId = models.CharField(max_length=100, default=0)
    addedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.addedOn
