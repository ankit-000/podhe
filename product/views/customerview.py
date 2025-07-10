import datetime
from django.shortcuts import render,redirect
from django.views import View
from product.forms import ReviewForm
from product.models import Category, Coupon, Product, ProductRating
from django.contrib import messages
from customer.models import Order, OrderItems, WishList

class details(View):
    def get(self,request,pid):
        product = Product.objects.get(id = pid)
        reviews = ProductRating.objects.filter(product=product,is_live=True)
        categories = Category.objects.all()
        args={}
        args['product'] = product
        args['reviews'] = reviews
        args['categories'] = categories
        form = ReviewForm()
        args['form'] = form
        return render(request,"product/details.html",args)
    
    def post(self,request,pid):
        form = ReviewForm(request.POST)
        orders = OrderItems.objects.filter(order__user__id=request.user.id)
        purchased = False
        for order in orders:
            if order.productId == pid:
                purchased = True
                break
        if purchased == False:
            messages.info(request,"Review can only be added by customers who has purchased this product!")
            return redirect(request.META.get('HTTP_REFERER'))  
        if form.is_valid():
            rform = form.save(commit=False)
            rform.user = request.user.id    
            rform.product = Product.objects.get(id=pid)
            rform.save()
            messages.success(request,"Your review was submitted successfully!")
            url = "{}/{}".format("/product/details",pid)
            return redirect(url)
        return redirect(request.META.get('HTTP_REFERER'))


def AddToCart(request):
   #pid = request.GET["pid"]   
   # productpin = Product.objects.get(id=pid).addedBy.address.pinCode
   # pin = request.session.get('pincode')
   # if pin == productpin:
   AddProductToCart(request)
   #else:
   #messages.error(request,"Sorry! This product does cannot be delivered to the pincode you selected!")     
   return redirect(request.META.get('HTTP_REFERER')) 


def BuyNow(request)  :
    AddProductToCart(request)
    return redirect("cartsummary")

def AddProductToCart(request):
    try:
        units = request.GET['qtybutton']    
        date = request.GET['date']    
        time = request.GET['time_period']    
    except:
        units = 1
    pid = request.GET["pid"]   
    cart = request.session.get("cart",{})        
    if cart is None:
        cart = {}       
    
    try:
        prodid = Product.objects.get(id=pid).id       
    except:
        messages.error(request,"No product found with this id!")            
        return redirect(request.META.get('HTTP_REFERER'))    
    cartitem = cart.get(str(prodid))
    
    if cartitem is None:
        quantity = units
    else:   
        quantity =cartitem["quantity"]
        quantity = int(quantity) + int(units)
        if quantity > 10:
           quantity = str(10)            
    if date!= "" and time != "":
        cart[str(pid)] = {"date":date,"time":time,"quantity":quantity}        
    request.session["cart"] = cart   

def UpdateCart(request,pid):
    cart = request.session.get("cart")
    cartitem = cart[str(pid)]
    cartitem['quantity'] = request.GET["qtybutton"]
    request.session["cart"] = cart 
    code = ""
    try:
        code = request.session["couponcode"]
        if not code is None:
            ApplyCoupon(request)
    except:
        pass
    return redirect("cartsummary")

def RemoveFromCart(request,pid):
    cart = request.session.get("cart")
    del cart[str(pid)]
    request.session["cart"] = cart 
    try:
        code = request.session["couponcode"]
        if not code is None:
            ApplyCoupon(request)
    except:
        pass
    return redirect("cartsummary")


def AddToWishlist(request,pid):
    if request.user.is_anonymous:
        messages.info(request,"You need to login before adding a product to your wishlist!")
        return redirect("/account/login")
    elif request.user.is_vendor:
        return redirect(request.META.get('HTTP_REFERER'))  
    try:
        Product.objects.get(id=pid)
        wishlist = WishList.objects.create(user=request.user.Customer,productId=pid)
        wishlist.save()
        messages.success(request,"Product added to your Wishlist!")
    except:
        pass
    return redirect(request.META.get('HTTP_REFERER'))    

def Wishlist(request):
    if request.user.is_anonymous:
        messages.info(request,"You need to login before viewing your WishList!")
        return redirect("/account/login")
    elif request.user.is_vendor:
        return redirect("home")
    wishlist = WishList.objects.filter(user=request.user.Customer)
    plist = []
    for w in wishlist:
        plist.append(w.productId)
    products = Product.objects.filter(id__in=plist)
    return render(request,"product/wishlist.html",{"products":products})

def RemoveFromWishList(request,pid):
    WishList.objects.filter(productId=pid, user = request.user.Customer).delete()
    return redirect("wishlist")

def ApplyCoupon(request):
    try:
        code = request.GET['couponcode']
    except:
        code = request.session["couponcode"]
    try:
        coupon = Coupon.objects.get(couponCode=code)
        discount = 0
        if coupon.currentRedemptions == coupon.maxRedemptions or coupon.validUpto < datetime.datetime.now():
            messages.error(request,"Sorry! This coupon is either invalid or has expired.")   
            return redirect(request.META.get('HTTP_REFERER'))   
        totalcartprice = 0
        cart = request.session.get("cart")
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            totalcartprice = totalcartprice + (product.productSalePrice * int(cart[str(product.id)]))
        if (totalcartprice * coupon.valueInPercent/100) >= coupon.maxDiscount:
            discount = coupon.maxDiscount
        else:
            discount = totalcartprice * coupon.valueInPercent/100
        request.session["discount"] = discount
        request.session["couponcode"] = code
    except:
        messages.error(request,"Sorry! This coupon is either invalid or has expired.")
    
    return redirect(request.META.get('HTTP_REFERER'))  


def RemoveCoupon(request):  
    try:
        del request.session["discount"]
        del request.session["couponcode"]
    except:
        pass
    return redirect(request.META.get('HTTP_REFERER'))  


class AddReview(View):
    def get(self,request,pid):
        orders = OrderItems.objects.filter(order__user__id=request.user.id)
        purchased = False
        for order in orders:
            if order.productId == pid:
                purchased = True
                break
        if purchased == False:
            messages.info(request,"Review can only be added by customers who has purchased this product!")
            return redirect(request.META.get('HTTP_REFERER'))  
        form = ReviewForm()
        return render(request,"product/addreview.html",{"form":form})
    
    def post(self,request,pid):
        form = ReviewForm(request.POST)
        orders = OrderItems.objects.filter(order__user__id=request.user.id)
        purchased = False
        for order in orders:
            if order.productId == pid:
                purchased = True
                break
        if purchased == False:
            messages.info(request,"Review can only be added by customers who has purchased this product!")
            return redirect(request.META.get('HTTP_REFERER'))  
        if form.is_valid():
            rform = form.save(commit=False)
            rform.user = request.user.id    
            rform.product = Product.objects.get(id=pid)
            rform.save()
            messages.success(request,"Your review was submitted successfully!")
            url = "{}/{}".format("/product/details",pid)
            return redirect(url)
        return redirect(request.META.get('HTTP_REFERER'))
