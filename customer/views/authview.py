from django.shortcuts import redirect, render
from django.views import View
from common.tasks import SendEmail
from common.models import User
import random




from customer.forms import LoginForm, ResendActivationForm, ResetPasswordForm, SetNewPasswordForm, SignupForm, otpForm
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

from customer.models import Customer


class Login(View):

    def get(self,request,type=''):
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm        
        return render(request,"customer/login.html",{"form":form}) 

    
    @method_decorator(sensitive_post_parameters("password"))
    @method_decorator(csrf_protect)
    def post(self,request,type=''):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None and user.is_customer:
                login(request,user)
                cart = request.session.get("cart")
                if cart is None:
                    cart = {}       
                if 'next' in request.POST:
                    return redirect(iri_to_uri(request.POST.get('next')))                    
                else:
                    if request.user.fullName is None:
                        messages.info(request,"Please fill in your profile details!")
                        return redirect("/customer/profile")
                    return redirect("/")
            else:
                messages.error(request,"Either your userid or password is incorrect or you account is not yet active.")                
        return render(request,'customer/login.html',{"form":form})

class SignUp(View):
    
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignupForm
        return render(request,"customer/signup.html",{"form":form})

    # @transaction.atomic
    @method_decorator(sensitive_post_parameters())
    def post(self,request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]            
            fullname=form.cleaned_data["fullname"]            
            user = User.objects.create_user(username=username,password=password)
            user.email = username   
            user.fullName = fullname
            user.is_active=False         
            user.is_customer = True
            user.save()
           
            otp = random.randint(100000,999999)
            customer = Customer.objects.create(user=user)
            customer.otpNumber = str(otp)
            customer.save()
            # if transaction.get_rollback():
            #     print("⚠️ Transaction is marked for rollback!")
            # else:
            #     print("✅ Transaction not rolled back.")
            SendActivationEmail(user,request,otp)
            print("Before setting session")
            # if transaction.get_rollback():
            #     print("⚠️ Transaction is marked for rollback!")
            # else:
            #     print("✅ Transaction not rolled back.")

            messages.success(request, "Please check your inbox for OTP Email!" )
            request.session["uname"] = user.username            
            return redirect("/customer/activate/")
        return render(request,"customer/signup.html",{"form":form} )

def SendActivationEmail(user,request,otp):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    subject = "Thank you for registering! Here is your account activation email."
    args={}
    args['mailto'] = user.username
    args['website'] = settings.WEBSITE_NAME
    args['domain'] = domain
    args['uid'] = uid
    args['token'] = token     
    args['otp'] = otp
    args["repname"] = settings.ADMIN_EMAIL
    body  = render_to_string("common/activateaccount.html",args)
    SendEmail(subject,body,settings.ADMIN_EMAIL,user.username)

    

class ResendActivationEmail(View):

    def get(self,request):
        form = ResendActivationForm
        return render(request,"customer/resendactivationemail.html",{"form":form})

    def post(self,request):
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username= form.cleaned_data['email'])
                if not user.is_active:
                    SendActivationEmail(user,request)
                    messages.success(request, 'You would receive an activation link on this email if this account is registered with us and is not active.')               
                    return render(request,"customer/resendactivationemail.html",{"form":form})
            except:
                messages.success(request, 'You would receive an activation link on this email if this account is registered with us and is not active.')               
                return render(request,"customer/resendactivationemail.html",{"form":form})        
        return render(request,"customer/resendactivationemail.html",{"form":form})


# class ActivateAccount(View):

#     def get(self,request,uidb64,token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except(TypeError,ValueError,OverflowError,User.DoesNotExist):
#             user = None
        
#         if user is not None and user.is_active == False and default_token_generator.check_token(user,token):
#             user.is_active= True
#             user.save()
#             messages.success(request,"Congrats, your account is active now! Please Login to continue.")            
#         else:
#             messages.error(request, 'The confirmation link is either invalid, expired or has already been used previously to activate account. Please review the link you used.')
#         return redirect("/customer/login/")


class ActivateAccount(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        form = otpForm        
        return render(request,"customer/activateaccount.html",{"form":form})

    def post(self,request):
        form = otpForm(request.POST)
        if form.is_valid():
            otp=form.cleaned_data["otp"]           
            user =User.objects.get(username=request.session.get("username"))
            cust = Customer.objects.get(user=user)
            if cust.otpNumber == otp:
                user.is_active= True
                user.save()
                messages.success(request,"Congrats your account is active now. Happy Shopping!")
            else:
                messages.error(request, 'Sorry the OTP you entered seems to be invalid! Please check once again.')
        return redirect("/customer/login/")



def Logout(request):
    logout(request)
    return redirect("/")


class ResetPassword(View):

    def get(self,request):
        form = ResetPasswordForm
        return render(request,"customer/resetpassword.html",{"form":form})

    def post(self,request):
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data["email"])
                token = default_token_generator.make_token(user)
                domain = get_current_site(request).domain
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                subject = "Forgot your password? No worries! Here is the link to reset your password."
                args={}
                args['mailto'] = user.username
                args['website'] = settings.WEBSITE_NAME
                args['domain'] = domain
                args['uid'] = uid
                args['token'] = token
                args["repname"] = settings.ADMIN_EMAIL
                body = render_to_string("common/resetaccountpassword.html",args)
                SendEmail(subject,body,settings.ADMIN_EMAIL,user.username)                
                messages.success(request,"If you have an account with us, you would get a password reset email. Please follow it to reset your account password.")                
            except:               
                messages.success(request,"If you have an account with us, you would get a password reset email. Please follow it to reset your account password.")                    
        return render(request,"customer/resetpassword.html",{"form":form})
                


class CreateNewPassword(View):
    
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,token):
            form=SetNewPasswordForm(user)
            return render(request,'customer/setnewpassword.html',{"form":form})
        else:
            messages.warning(request, ('The reset password link is either invalid or has expired, please review the link you clicked.'))
            return redirect('/')     

    def post(self,request,uidb64,token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        form=SetNewPasswordForm(user,request.POST)
        if form.is_valid():            
            user.set_password(form.cleaned_data["new_password1"])
            user.save()            
            messages.success(request,"Congrats, your password was sucessfully reset! Please login to continue.")            
            return redirect("/customer/login/")       
        return render(request,'customer/setnewpassword.html',{"form":form})
