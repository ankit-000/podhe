from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect
from product.forms import ProductForm, ProductMediaForm
from product.models import Product, ProductMedia
from django.contrib import messages
from django.views.generic.edit import UpdateView


class Products(View):
    @method_decorator(login_required)       
    def get(self,request):
        products = Product.objects.filter(addedBy = request.user.Vendor,is_visible=True)
        return render(request,"product/products.html",{"products":products})

class AddProduct(UpdateView):    
    def get(self,request,pid=""):
        try:
            address = request.user.Vendor.address
            if request.user.Vendor.address.pinCode == '' or request.user.Vendor.address.pinCode is None:
                messages.error(request,"You need to add your address details before you can add a product! ")
        except:
            messages.error(request,"You need to add your address details before you can add a product! ")
            return redirect("vendor:address")
        
        if pid =="":
            form = ProductForm
        else:            
            product = Product.objects.filter(id=pid).first()            
            if not product is None:                                
                form = ProductForm(instance=product)                
        return render(request,"product/addproduct.html",{"form":form})

    def post(self,request,pid=""):
        if pid =="":
            form = ProductForm(request.POST)
        else:            
            product = Product.objects.filter(id=pid).first()
            if not product is None:
                form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            pdata = form.save(commit=False)
            User = request.user
            pdata.addedBy = User.Vendor
            pdata.is_visible = True
            pdata.save()            
            messages.success(request,"Product saved successfully!")
            return redirect("products")
        return render(request,"product/addproduct.html",{"form":form})


class DeleteProduct(View):
    def post(self,request,pid):
        try:
            product = Product.objects.get(id=pid, addedBy_id=request.user.Vendor.id)
            product.is_visible = False
            product.save()            
            messages.success(request,"Product deleted successfully!")
        except:
            messages.error(request,"Selected product cannot be deleted. Please check the link you clicked")
        return redirect("products")   


class AddProductMedia(View):
    
    def get(self,request,pid):        
        media = ProductMedia.objects.filter(product_id=pid)
        args={}
        args["media"] = media        
        form=ProductMediaForm()    
        args["form"] = form
        return render(request,"product/addproductmedia.html",args)        
    
    def post(self,request,pid):
        media = ProductMedia.objects.filter(product_id=pid)
        args={}
        args["media"] = media        
        form=ProductMediaForm(request.POST,request.FILES)            
        args["form"] = form

        if form.is_valid():
            tform = form.save(commit=False)
            tform.product_id = pid
            tform.save()
            messages.success(request,"Media file saved successfully!")
            url= "{}/{}/".format("/product/addmedia",pid)
            return redirect(url)        
        return render(request,"product/addproductmedia.html",args)        

class DeleteProductMedia(View):
    def post(self,request,pid,mid):
        try:
            media = ProductMedia.objects.get(id=mid)
            if media.mainimage == True:
                messages.error(request,"Primary media file cannot be deleted! Please select another file as primary and try again.")    
            else:
                ProductMedia.objects.get(id=mid).delete()                    
                messages.success(request,"Media file deleted successfully!")
        except:
            messages.error(request,"Selected media file not found in database! Please check the link you have clicked.")
        url= "{}/{}/".format("/product/addmedia",pid)
        return redirect(url)        


class MakePrimary(View):
    def post(self,request,pid,mid):
        try:
            mediafile = ProductMedia.objects.get(id=mid)
            mfiles = ProductMedia.objects.filter(product_id=pid)
            for m in mfiles:
                m.mainimage = False
                if m.id == mid:
                    m.mainimage = True
                m.save()                        
            messages.success(request,"Media file updated successfully!")
        except:
            messages.error(request,"Selected media file not found in database! Please check the link you have clicked.")
        url= "{}/{}/".format("/product/addmedia",pid)
        return redirect(url)    
