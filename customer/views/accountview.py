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
from customer.models import Order, UserAddress
from product.models import Product


class Profile(View):
    @method_decorator(login_required)
    def get(self,request):
        args={}
        address= UserAddress.objects.filter(user=request.user.Customer).first()        
        orders = Order.objects.filter(user=request.user)
        userform = EditUserForm(instance=request.user) 
        passwordform = ChangeUserPasswordForm(self.request.user)
        args['address'] = address        
        args['orders'] = orders
        args['userform'] = userform         
        args['passwordform'] = passwordform         
        return render(request,'customer/profile.html',args)
    
    @transaction.atomic
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    def post(self,request):
        args={}
        userform=EditUserForm(request.POST,instance=request.user)        
        passwordform=ChangeUserPasswordForm(self.request.user,request.POST)
        args['userform'] = userform                   
        if userform.is_valid():
            userform.save()                   
            messages.success(request,"Details changed successfully!")        
            return redirect("/customer/profile")                 
        return render(request,"customer/profile.html",args)

class ProfileDetails(View):
    @method_decorator(login_required)
    def get(self,request):
        args={}
        userform = EditUserForm(instance=request.user)        
        args['userform'] = userform        
        return render(request,"customer/profiledetails.html",args)

    @transaction.atomic
    @method_decorator(login_required)
    def post(self,request):
        args={}
        userform=EditUserForm(request.POST,instance=request.user)        
        args['userform'] = userform                                                
        messages.success(request,"Profile Details saved successfully!")
        if userform.is_valid(): 
            userform.save()       
            if len(UserAddress.objects.filter(user=request.user.Customer)) == 0:
                messages.info(request,"Please fill in your address details!")
                return redirect("/customer/address")     
            messages.success(request,"Profile Details saved successfully!")            
        return render(request,"customer/profiledetails.html",args) 

class ChangePassword(View):

    @method_decorator(login_required)
    @method_decorator(csrf_protect)    
    def get(self,request):
        form = ChangeUserPasswordForm(self.request.user)
        return render(request,"customer/changepassword.html",{"form":form})

    @method_decorator(sensitive_post_parameters())
    def post(self,request):
        form=ChangeUserPasswordForm(self.request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Password changed successfully! Please login again.")
            logout(request)
            return redirect("login")
        return render(request,"customer/changepassword.html",{"form":form})


def AllAddress(request):
    addresses = UserAddress.objects.filter(user=request.user.Customer, is_active=True)
    return render(request,"customer/myaddresses.html",{"addresses":addresses})

class Address(View):
    def get(self,request,id=0):              
        if id==0:            
            form = AddressForm()            
        else:
            try:
                address = UserAddress.objects.get(id=id,user=request.user.Customer)
                form = AddressForm(instance=address)
            except:
                pass        
        return render(request,"customer/address.html",{"form":form})  
    
    @transaction.atomic
    def post(self,request,id=0):        
        if id==0:
            form = AddressForm(request.POST)
        else:
            try:
                address = UserAddress.objects.get(id=id,user=request.user.Customer)
                form = AddressForm(request.POST,instance=address)
            except:
                pass
            
        if form.is_valid():
            cform = form.save(commit=False)
            cform.user = request.user.Customer
            cform.save()            
            messages.success(request,"Address details saved successfuly!")
            return redirect("profile")        
        return render(request,"customer/address.html",{"form":form}) 


# def DeleteAddress(request,id):
#     try:
#         address = UserAddress.objects.get(id=id,user=request.user.Customer)
#         address.is_active = False
#         address.save()
#     except:
#         return redirect("myaddresses")     
#     messages.success(request,"Address deleted successfully!")
#     return redirect("myaddresses")     

# def SetAddressAsDefault(request,id):    
#     addresses = UserAddress.objects.filter(user=request.user.Customer)
#     for address in addresses:
#         if address.id==id:
#             address.is_primary = True
#         else:
#             address.is_primary = False
#         address.save()
#     return redirect("myaddresses")     
    
    

