from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, UsernameField
from django import forms
from common.models import User
from django.contrib.auth import password_validation

from vendor.models import STATES, ACTYPE, Vendor, VendorAddress, VendorBankDetails


# Account Forms----------------------------------------------------------------------------------------------------------------------------------
class EditUserForm(forms.ModelForm):   
    
    class Meta:
        model=User
        fields = ["fullName","gender","contactNumber"]

class VendorProfile(forms.ModelForm):
    class Meta:
        model=Vendor
        fields = ["companyName"]
        

class VendorAddressForm(forms.ModelForm):
    pinCode = forms.IntegerField()    
    state = forms.ChoiceField(choices= STATES)
    class Meta:
        model=VendorAddress
        fields=["address1","address2","landMark","state","pinCode"]

    def clean(self):
        cleaned_data = super(VendorAddressForm, self).clean()
        pincode = cleaned_data.get("pinCode")
        if len(str(pincode)) < 6 or len(str(pincode))>6:
            self.add_error("pinCode","Pincode must be a 6 digit number!")

class BankDetailsForm(forms.ModelForm):
    confirmAccountNumber = forms.CharField(max_length=30) 
    accountType = forms.ChoiceField(choices=ACTYPE)
    class Meta:
        model = VendorBankDetails
        exclude = ["user"]

    def clean(self):
        cleaned_data = super(BankDetailsForm, self).clean()
        accountNumber = cleaned_data.get("bankAccountNumber")
        confirmAccount = cleaned_data.get("confirmAccountNumber")

        if confirmAccount != accountNumber:
            self.add_error('confirmAccountNumber', "Account Numbers does not match!")
        return cleaned_data

class ResetPasswordFormV(PasswordResetForm):
    email=forms.CharField(label="Email Address", widget=forms.EmailInput(attrs={"class":"form-control"}))