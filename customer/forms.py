from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, UsernameField
from django import forms
from common.models import User 
from django.contrib.auth import password_validation

from customer.models import STATES, UserAddress
from django.core.exceptions import ValidationError




# Auth Forms----------------------------------------------------------------------------------------------------------------------------------

class LoginForm(AuthenticationForm):
    username=UsernameField(label="Email Address", widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

    error_messages = {
        'invalid_login': (
            "An error occurred while trying to login! Either your userid or password is incorrect or you account is not yet active. Please review."
        ),
        'inactive': "This account is inactive.",
    }

class otpForm(forms.Form):
    otp = forms.CharField(label="OTP Number", widget=forms.TextInput(attrs={"class":"form-control"}))    
    

class SignupForm(UserCreationForm):
    fullname=forms.CharField(label="Full Name", widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={"class":"form-control"}))
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(email__iexact=username).exists():
            raise forms.ValidationError("This email is already registered. Please try another email address")
        return username

    class Meta(UserCreationForm.Meta):
        model=User
        fields=["username","password1","password2"]  

class ResendActivationForm(forms.Form):
    email=forms.CharField(label="Email Address", widget=forms.EmailInput(attrs={"class":"form-control"}))

class ResetPasswordForm(PasswordResetForm):
    email=forms.CharField(label="Email Address", widget=forms.EmailInput(attrs={"class":"form-control"}))

class SetNewPasswordForm(SetPasswordForm):    
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}),help_text="Please enter the same password as before, for verification.")

# Account Forms----------------------------------------------------------------------------------------------------------------------------------
class ChangeUserPasswordForm(PasswordChangeForm):    
    old_password=forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2=forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"})) 

class EditUserForm(forms.ModelForm):   
    
    class Meta:
        model = User
        fields = ["fullName","gender","contactNumber"]

# class AddressForm(forms.ModelForm):    
            #   state = forms.ChoiceField(choices= STATES)
            #   class Meta:
                #  model = UserAddress
                #  fields=["address1","address2","landMark","city","state","pinCode","contactPerson","contactNumber"]
 
            #   def clean(self):
                #   cleaned_data = super(AddressForm, self).clean()
                #   pincode = cleaned_data.get("pinCode")
                #   if len(str(pincode)) < 6 or len(str(pincode)) > 6:
                    #  self.add_error("pinCode","Pincode must be a 6 digit number!")
# ✅ Define your allowed pincodes
ALLOWED_PINCODES = list(set([
    '110001', '110002', '110003', '110004', '110005', '110006', '110007',
    '110008', '110009', '110010', '110011', '110012', '110013', '110014',
    '110015', '110016', '110017', '110018', '110019', '110020', '110021',
    '110022', '110023', '110024', '110025', '110026', '110027', '110028',
    '110029', '110030', '110031', '110032', '110033', '110034', '110035',
    '110036', '110037', '110038', '110039', '110040', '110041', '110042',
    '110043', '110044', '110045', '110046', '110047', '110048', '110049',
    '110050', '110051', '110052', '110053', '110054', '110055', '110056',
    '110057', '110058', '110059', '110060', '110061', '110062', '110063',
    '110064', '110065', '110066', '110067', '110068', '110069', '110070',
    '110071', '110072', '110073', '110074', '110075', '110076', '110077',
    '110078', '110079', '110080', '110081', '110082', '110083', '110084',
    '110085', '110086', '110087', '110088', '110089', '110090', '110091',
    '110092', '110093', '110094', '110095', '110096', '110097', '110098',
    '110099', '110100', '110000',
]))

class AddressForm(forms.ModelForm):    
    state = forms.ChoiceField(choices=STATES)

    class Meta:
        model = UserAddress
        fields = ["address1", "address2", "landMark", "city", "state", "pinCode", "contactPerson", "contactNumber"]

    def clean_pinCode(self):
        pinCode = str(self.cleaned_data.get("pinCode"))

        # ✅ Check it's numeric and 6 digits
        if not pinCode.isdigit() or len(pinCode) != 6:
            raise ValidationError("Pincode must be a 6-digit number!")

        # ✅ Check if pincode is in allowed list
        if pinCode not in ALLOWED_PINCODES:
            raise ValidationError("We currently do not deliver to this pincode.")

        return pinCode
