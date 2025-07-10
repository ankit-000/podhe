from email.headerregistry import Address
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import razorpay
from customer.models import RazorOrder, UserAddress

from product.models import Product




@login_required
def cartsummary(request):
    if request.user.is_vendor:
        return redirect("/")
    #address = UserAddress.objects.filter(user=request.user.Customer, is_primary=True).first()  
    #if address is None or address.address1  == "" or address.address1 is None:
    #   messages.info(request,"We need your default address details before you can place an order!")    
    #  return redirect('/customer/myaddresses')
    if request.user.fullName is None:
        messages.info(request,"Please complete your profile details before placing an order!")
        return redirect('/customer/profile')    
    cart = request.session.get("cart")
    if cart is None:    
        cart={}
        request.session["cart"] = cart  
    cart = request.session.get("cart")
    products = Product.objects.filter(id__in=cart.keys()) 
    # addresses = UserAddress.objects.filter(user=request.user.Customer, is_active=True)   
    address = ""
    try:
        address = UserAddress.objects.get(user=request.user.Customer)
    except:
        messages.error(request,"Please add an address to continue!")
        return redirect("/customer/address")
    request.session["addressid"] = address.id
    addressid = request.session.get("addressid")
    couponcode = ''
    couponcode = request.session.get("couponcode")
    if request.POST:
        addressid=int(request.POST['group1'])
        request.session["addressid"] = addressid
        return render(request,"home/cartsummary.html",{"products":products,"addressid":addressid,"couponcode":couponcode,"address":address})
    elif not addressid is None:
        return render(request,"home/cartsummary.html",{"products":products,"addressid":int(addressid),"couponcode":couponcode,"address":address})
    else:
        return render(request,"home/cartsummary.html",{"products":products,"couponcode":couponcode,"address":address})
    

def MakePayment(request):
    aid = request.session.get("addressid")
    if aid is None:
        messages.info(request,"Please select or add an address!")
        return redirect("/cartsummary")

    cart = request.session.get("cart")
    delcart = []
#    addressid = request.session.get("addressid")
#   address = UserAddress.objects.filter(id=addressid).first()
#    if not address is None:
#        addpin = address.pinCode
#        for key in cart.keys():
#            product = Product.objects.filter(id=key).first()
#            if product.addedBy.address.pinCode != addpin:
#                delcart.append(key)
#        if len(delcart) > 0:
#            for d in delcart:
#                del cart[str(d)]
#            request.session["cart"] = cart
#            messages.info(request,"Some Products may have been removed from your cart based on you selected address! Please review.")
#           return redirect('cartsummary')



    orderamt = float(request.POST["orderamt"])
    razorclient = razorpay.Client(auth=(settings.RAZORPAYID,settings.RAZORPAYKEY))
    data = {'amount':(orderamt*100),'currency':'INR'}
    razorOrder = razorclient.order.create(data)

    
    args={}
    cart = request.session.get("cart")
    products = Product.objects.filter(id__in=cart.keys())
    args['products'] = products
    args['orderid'] = razorOrder['id']
    args['username'] = request.user.fullName
    args['useremail'] = request.user.username
    args['contactno'] = request.user.contactNumber
    args['key'] = settings.RAZORPAYID
    args['coupon'] = "coupon"
    args['addressid'] = request.session.get("addressid")
    args['surl'] = "https://" + str(get_current_site(request)) +  "/customer/ordersuccess/"


    address = UserAddress.objects.filter(id=request.session.get("addressid")).first()
    args['address'] = address
    cart = request.session.get('cart')
    RazorOrder.objects.create(razorOrderId=razorOrder['id'],userId=request.user.id,cartDict=str(cart))
    return render(request,"home/makepayment.html", args)
