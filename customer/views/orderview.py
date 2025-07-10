from django.http import HttpResponse
from django.shortcuts import render,redirect
from common.models import Invoice
from customer.models import Order, OrderItems, RazorOrder, UserAddress
from common.tasks import SendEmail
from product.models import Category, Coupon, Product
import razorpay
from django.conf import settings
import ast
import pdfkit
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from vendor.models import Vendor




@csrf_exempt
@transaction.atomic
def OrderPlaced(request):
    razorclient = razorpay.Client(auth=(settings.RAZORPAYID,settings.RAZORPAYKEY))
    params_dict = {
            'razorpay_order_id': request.POST['razorpay_order_id'],
            'razorpay_payment_id': request.POST['razorpay_payment_id'],
            'razorpay_signature': request.POST['razorpay_signature']
        }

    if razorclient.utility.verify_payment_signature(params_dict) is None:
        resp = razorclient.payment.fetch(request.POST['razorpay_payment_id'])
        coupon = resp["notes"]['coupon']
        address = resp["notes"]['addressid']
        totalamount = float(resp["amount"])/100
        order = CreateOrder(request,coupon,address,totalamount,request.POST['razorpay_order_id'])
        url = "{}/{}".format("/customer/ordersuccessful",order.id)
        return redirect(url)
    else:
        url = "{}/{}".format("/orderfailed",order.id)
        return redirect(url)

def OrderFailed(request):
    return render(request,"home/paymentfailed.html")

@transaction.atomic
def CreateOrder(request,coupon,address,totalamt,razororderid):
    purchasedproducts = ast.literal_eval(RazorOrder.objects.get(razorOrderId=razororderid).cartDict)
    razorclient = razorpay.Client(auth=(settings.RAZORPAYID,settings.RAZORPAYKEY))
    coupon = Coupon.objects.filter(couponCode=coupon).first()
    if coupon is None:
        coupon=''

    discountamt = 0
    try:
        discountamt = request.session["discount"]
    except:
        pass


    order = Order.objects.create(discount=discountamt,user=request.user,addressid=address,couponCode=coupon,taxOnOrder=request.session.get("tax"),orderTotal=totalamt,orderStatus="Placed",razorOrderId=razororderid,razorPaymentId=request.POST['razorpay_payment_id'],razorSignature =request.POST['razorpay_signature'])
    AddItemsToOrder(request,order,purchasedproducts,coupon)
    if coupon != '':
        UpdateCoupon(coupon)
    

    #capture payment on razorpay
    payment_id = request.POST['razorpay_payment_id']
    payment_amount = int(totalamt*100)
    payment_currency = "INR"    
    resp=""
    try:
        resp = razorclient.payment.capture(payment_id, payment_amount, {"currency":payment_currency})
    except:        
        pass
        # if resp !=''    :
        #     raise ValueError(resp)
    return order
    


def OrderSuccess(request,orderid):
    cart = request.session.get("cart")
    order = Order.objects.filter(id=orderid).first()
    if cart:
        cart={}
        request.session["cart"] = cart    
    SendOrderEmail(request,order)   
    return render(request,"customer/orderplaced.html",{"order":order})

def SendOrderEmail(request,order):
    domain = get_current_site(request).domain
    url="{}/{}/{}/".format(domain,'customer/printinvoice',order.id)
    pdf = GeneratePDFfromHTML(request,url)    
    SendEmail("Thank you for your order!", "Thanks for your order today. We have attached an invoice for your order. Please review","order@podhewale.com",request.user.username,"InvOrd-" + order.orderId,pdf)


def GeneratePDFfromHTML(request,htmltemplate,args={}):           
        cookie_list = request.COOKIES
        options = {
            'no-background':None,
        'cookie' : [
            ('csrftoken', cookie_list['csrftoken']),
            ('sessionid', cookie_list['sessionid']),
            ]
        }
        return pdfkit.from_url(htmltemplate,False,options)


def GetInvoice(request,orderid):    
    domain = get_current_site(request).domain
    order = Order.objects.filter(id=orderid).first()
    url="{}/{}/{}/".format(domain,'customer/printinvoice',order.id)
    pdf = GeneratePDFfromHTML(request,url)    
    filename = Order.objects.filter(id=order.id).first().orderId + ".pdf"
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response

def PrintInvoice(request,orderid):
    try:
        order=Order.objects.get(id=orderid,user=request.user)        
        address = UserAddress.objects.filter(id=order.addressid).first()
        invoice = Invoice.objects.filter(order=order.orderId).first()
        if invoice == None:
            invoice = Invoice.objects.create(order=order.orderId)            
        vendors=[]
        for oitem in order.orderitems_set.all():
            vendors.append(Vendor.objects.filter(id=oitem.vendorId).first())
    except:
        messages.error(request,"Sorry! No order with this id found in your account.")
        return redirect("orders")
    return render(request,"customer/printinvoice.html",{"order":order,"address":address,"vendors":vendors,"invoice":invoice})

def AddItemsToOrder(request,order,purchasedproducts,coupon):
    products = Product.objects.filter(id__in=purchasedproducts.keys())      
    try:
        coupon = Coupon.objects.filter(couponCode=request.session["couponcode"]).first()
    except:
        pass
    cart = request.session.get("cart")
    discountpercent= 0
    maxdiscount = 0
    totaldiscount = 0
    if coupon is None or coupon == '':
        products = Product.objects.filter(id__in=purchasedproducts.keys())
        for p in products:
                OrderItems.objects.create(
                    order=order,
                    productId = p.id,
                    productName = p.productName,
                    unitPrice = p.productMRP,
                    listPrice = p.productSalePrice,
                    quantity= int(cart.get(str(p.id["quantity"]))),
                    paidPrice = (p.productSalePrice * int(cart.get(str(p.id["quantity"])))),
                    taxAmount = (p.productSalePrice * int(cart.get(str(p.id["quantity"])))) * (p.taxPercent/100),
                    discountAmount = 0,
                    vendorId = p.addedBy.user.Vendor.id,
                    userId = request.user.id,
                    appointmentTime = int(cart.get(str(p.id["time"]))),
                    appointmentDate = int(cart.get(str(p.id["date"]))),

                )
    else:
        discountpercent = coupon.valueInPercent
        maxdiscount = coupon.maxDiscount
        products = Product.objects.filter(id__in=purchasedproducts.keys())
        for p in products:
            totaldiscount = totaldiscount + (p.productSalePrice * int(cart.get(str(p.id["quantity"]))) * discountpercent/100)

        if totaldiscount > maxdiscount:
            perunitdiscount = 0
            totalunits = 0
            for key in cart.keys():
                totalunits = totalunits +int(cart.get(str(p.id["quantity"])))
            perunitdiscount = maxdiscount / totalunits

            for p in products:
                OrderItems.objects.create(
                    order=order,
                    productId = p.id,
                    productName = p.productName,
                    unitPrice = p.productMRP,
                    listPrice = p.productSalePrice,
                    quantity= int(cart.get(str(p.id["quantity"]))),
                    paidPrice = (p.productSalePrice * int(cart.get(str(p.id["quantity"])))) - (perunitdiscount*int(cart.get(str(p.id["quantity"])))),
                    taxAmount = (p.productSalePrice * int(cart.get(str(p.id["quantity"])))) - (perunitdiscount*int(cart.get(str(p.id["quantity"])))) * (p.taxPercent/100),
                    discountAmount = (perunitdiscount*int(cart.get(str(p.id["quantity"])))),
                    vendorId = p.addedby.user.Vendor.id,
                    userId = request.user.id,
                    appointmentTime = int(cart.get(str(p.id["time"]))),
                    appointmentDate = int(cart.get(str(p.id["date"]))),
                )
        else:
            for p in products:
                OrderItems.objects.create(
                    order=order,
                    productId = p.id,
                    productName = p.productName,
                    unitPrice = p.productMRP,
                    listPrice = p.productSalePrice,
                    quantity= int(cart.get(str(p.id["quantity"]))),
                    paidPrice = (p.productSalePrice * int(cart.get(str(p.id["quantity"])))) - (discountpercent/100*p.productSalePrice*int(cart.get(str(p.id["quantity"])))),
                    taxAmount = ((p.productSalePrice * int(cart.get(str(p.id["quantity"])))) - (discountpercent/100*p.productSalePrice*int(cart.get(str(p.id["quantity"]))))) * (p.taxPercent/100),
                    discountAmount = (discountpercent/100*p.productSalePrice*int(cart.get(str(p.id["quantity"])))),
                    vendorId = p.addedBy.user.Vendor.id,
                    userId = request.user.id
                )
        del request.session["discount"]
        del request.session["couponcode"]


def UpdateCoupon(coupon):
    coupon.currentRedemptions = coupon.currentRedemptions+1
    coupon.save()


def Orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,"customer/orders.html",{"orders":orders})

@transaction.atomic
def CancelOrder(request,oid):    
    order = Order.objects.filter(id=oid).first()
    if not order is None and (order.orderStatus == "Processing" or order.orderStatus =="packed"):
        order.orderStatus = "Cancelled"
        order.save()
        InititateRefundOnOrder(order)
        messages.success(request,"Your order has been cancelled as per your request! Your refund would be initiated soon.")
    return redirect(request.META.get('HTTP_REFERER'))  

def InititateRefundOnOrder(order):
    client = razorpay.Client(auth=(settings.RAZORPAYID,settings.RAZORPAYKEY))
    payment_id = order.razorPaymentId
    payment_amount = int(order.orderTotal*100)
    resp = client.payment.refund(payment_id, payment_amount) 


def ReturnProduct(request,orderitemid):
    orderitem = OrderItems.objects.filter(id = orderitemid, userId=request.user.Customer.id).first()
    orderitem.returnRequested = True
    orderitem.returnStatus = "Return Requested"
    orderitem.save()
    # InititateRefundOnProduct(orderitem)
    messages.success(request,"Your return has been initiated! Refund amount should be reflected in the original account payment was made from in about 7-10 days.")
    return redirect("orders")


def InititateRefundOnProduct(orderitem):
    client = razorpay.Client(auth=(settings.RAZORPAYID,settings.RAZORPAYKEY))
    payment_id = orderitem.order.razorPaymentId
    payment_amount = int(orderitem.paidPrice*100)
    resp = client.payment.refund(payment_id, payment_amount)
