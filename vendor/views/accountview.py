import datetime
from email.headerregistry import Address
from django.shortcuts import redirect, render
from django.views import View
from common.models import User
from customer.forms import AddressForm, ChangeUserPasswordForm, EditUserForm, LoginForm, ResendActivationForm, ResetPasswordForm, SetNewPasswordForm, SignupForm
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text, iri_to_uri

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from customer.models import Order, OrderItems
from product.models import Product
from vendor.forms import BankDetailsForm, VendorAddressForm, VendorProfile
from vendor.models import Vendor, VendorAddress, VendorBankDetails

def Profile(request):
    args={}
    address= VendorAddress.objects.filter(user=request.user.Vendor).first()
    orders = OrderItems.objects.filter(vendorId = request.user.Vendor.id).count            
    args['address'] = address
    args['orders'] = orders
    return render(request,'vendor/profile.html',args)

class ProfileDetails(View):
    @method_decorator(login_required)
    def get(self,request):
        args={}
        userform = EditUserForm(instance=request.user)   
        vendorform = VendorProfile(instance=request.user.Vendor)     
        args['userform'] = userform        
        args['vendorform'] = vendorform        
        return render(request,"vendor/profiledetails.html",args)

    @transaction.atomic
    @method_decorator(login_required)
    def post(self,request):
        args={}
        userform=EditUserForm(request.POST,instance=request.user)        
        vendorform=VendorProfile(request.POST,instance=request.user)        
        args['userform'] = userform             
        args['vendorform'] = vendorform                                    
        messages.success(request,"Profile Details saved successfully!")
        if userform.is_valid() and vendorform.is_valid(): 
            userform.save()
            vendor = Vendor.objects.get(user=request.user)
            vendor.companyName = request.POST['fullName']
            vendor.save()
            if request.user.is_vendor and len(VendorAddress.objects.filter(user=request.user.Vendor)) == 0:
                messages.info(request,"Please add your address details here.")
                return redirect("/vendor/address")
            messages.success(request,"Profile Details saved successfully!")            
        return render(request,"vendor/profiledetails.html",args) 

class ChangePassword(View):

    @method_decorator(login_required)
    @method_decorator(csrf_protect)    
    def get(self,request):
        form = ChangeUserPasswordForm(self.request.user)
        return render(request,"vendor/changepassword.html",{"form":form})

    @method_decorator(sensitive_post_parameters())
    def post(self,request):
        form=ChangeUserPasswordForm(self.request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Password changed successfully! Please login again.")
            logout(request)
            return redirect("login")
        return render(request,"vendor/changepassword.html",{"form":form})

class Address(View):
    def get(self,request):                     
        address=None
        try:
            address = VendorAddress.objects.get(user=request.user.Vendor)
        except:
            pass
        if address==None:
            form = VendorAddressForm()
        else:
            form = VendorAddressForm(instance=address)
        return render(request,"vendor/address.html",{"form":form})  
    
    @transaction.atomic
    def post(self,request):               
        address=None
        try:
            address = VendorAddress.objects.get(user=request.user.Vendor)
        except:
            pass
        if address == None:
            form = VendorAddressForm(request.POST)
        else:
            form = VendorAddressForm(request.POST,instance=address)
        if form.is_valid():
            vform = form.save(commit=False)
            vform.user = request.user.Vendor
            vform.save()
            if request.user.is_vendor and len(VendorBankDetails.objects.filter(user=request.user.Vendor)) == 0:
                messages.info(request,"Please add your bank details here.")
                return redirect("/vendor/bankdetails")
            messages.success(request,"Address details saved successfully!")            
        return render(request,"vendor/address.html",{"form":form}) 


class BankDetails(View):
    def get(self,request):                     
        bankdetails=None
        try:
            bankdetails = VendorBankDetails.objects.get(user=request.user.Vendor)
        except:
            pass
        if bankdetails==None:
            form = BankDetailsForm()
        else:
            form = BankDetailsForm(instance=bankdetails)
        return render(request,"vendor/bankdetails.html",{"form":form})  
    
    @transaction.atomic
    def post(self,request):               
        bankdetails=None
        try:
            bankdetails = VendorBankDetails.objects.get(user=request.user.Vendor)
        except:
            pass
        if bankdetails == None:
            form = BankDetailsForm(request.POST)
        else:
            form = BankDetailsForm(request.POST,instance=bankdetails)
        if form.is_valid():
            vform = form.save(commit=False)
            vform.user = request.user.Vendor
            vform.save()
            if len(Product.objects.filter(addedBy=request.user.Vendor)) == 0:
                messages.info(request,"Please add products and review the orders from this dashboard.")
                return redirect("/vendor/dashboard")

            messages.success(request,"Bank details saved successfully!")            
        return render(request,"vendor/bankdetails.html",{"form":form}) 


def Dashboard(request):
    orders = OrderItems.objects.filter(vendorId=request.user.Vendor.id)
    products = Product.objects.filter(addedBy = request.user.Vendor).count()    
    sales = OrderItems.objects.filter(vendorId=request.user.Vendor.id,order__orderedOn__date=datetime.date.today()).count()
    totalsales = 0
    for order in orders:
        totalsales = totalsales + order.paidPrice
    args={}
    args['orders'] = orders.count()
    args['products'] = products
    args['sales'] = sales
    args['totalsales'] = totalsales
    return render(request,"vendor/dashboard.html",args)
    
    

