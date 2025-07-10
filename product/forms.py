from django import forms
from django.db.models import fields
from django.forms.widgets import Select, SelectMultiple
from .models import Product, ProductMedia, ProductRating
from ckeditor.widgets import CKEditorWidget

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

class ProductForm(forms.ModelForm):
    #tagCloud = forms.CharField(widget=SelectMultiple(choices=OPTS))  
    productDescription = forms.CharField(max_length=5000, widget=CKEditorWidget())   
    
    class Meta:
        model = Product
        exclude = ['addedBy','saleCounter']

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        price = cleaned_data.get("productMRP")        
        discountedprice = cleaned_data.get("productSalePrice")        

        if discountedprice > price:
            self.add_error('productSalePrice', "Sale Price cannot be more than price (MRP)!")
        return cleaned_data

class ProductMediaForm(forms.ModelForm):
    productmedia =  forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={"class":"form-control-file","accept":".mp4,.mkv,.jpg,.jpeg,.png"}))    
    
    class Meta:
        model = ProductMedia    
        exclude = ["product"]

class ReviewForm(forms.ModelForm):    
    class Meta:
        model = ProductRating
        fields = ["rating","reviewSubject",'reviewDescription']
