
from datetime import datetime
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from common.models import Invoice
from customer.models import Order, OrderItems, UserAddress
from django.contrib.sites.shortcuts import get_current_site
import pdfkit
from django.contrib import messages

from vendor.models import Vendor

def Orders(request):
    orders = OrderItems.objects.filter(vendorId = request.user.Vendor.id).order_by('-order__orderedOn')
    if request.POST:
        try:
            status = request.POST['orderstatus']
        except:
            messages.error(request,"Please select order status")
            return redirect("vendor:orders")
        awb = request.POST['trackingid']
        trackingprov = request.POST['trackingProvider']
        orderid = request.POST['orderid']
        order = Order.objects.filter(id=orderid).first()
        order.orderStatus = status
        order.trackingInfo = awb
        order.trackingProvider = trackingprov 
        if request.POST['deliverDate'] !='':
            order.deliveryDate = request.POST['deliverDate']
        if status == "Shipped":
            order.shippedon = datetime.now()       
        order.save()
    return render(request,"vendor/orders.html",{"orders":orders})

def GenerateInvoice(request,orderid):
    domain = get_current_site(request).domain
    url="{}/{}/{}/".format(domain,'vendor/printinvoice',orderid)
    pdf = GenerateInvoicePDF(request,url)
    filename = Order.objects.filter(id=orderid).first().orderId + ".pdf"
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response
    


def GenerateInvoicePDF(request,htmltemplate,args={}):           
        cookie_list = request.COOKIES
        options = {
            'no-background':None,
        'cookie' : [
            ('csrftoken', cookie_list['csrftoken']),
            ('sessionid', cookie_list['sessionid']),
            ]
        }
        return pdfkit.from_url(htmltemplate,False,options)


def PrintInvoice(request,orderid):
    try:
        orderitems=OrderItems.objects.filter(order_id=orderid,vendorId=request.user.Vendor.id)        
        address = UserAddress.objects.filter(id=orderitems.first().order.addressid).first()                
        vendor = Vendor.objects.filter(id=orderitems.first().vendorId).first()
        invoice = Invoice.objects.filter(order=orderid).first()
        if invoice == None:
            invoice = Invoice.objects.create(order=orderid)         
        args={}
        args['orderitems'] = orderitems
        args['address'] = address
        args['vendor'] = vendor
        order = Order.objects.filter(id=orderid).first()
        args['orderid'] = order.orderId
        args['orderdate'] = order.orderedOn
        args['couponcode'] = order.couponCode
        args['invoiceNo'] = invoice.invoiceNo
        args['invoiceDate'] = invoice.invoiceDate
        ordertotal = 0
        taxtotal = 0
        disctotal = 0
        
        for item in orderitems:
            ordertotal = ordertotal + item.paidPrice
            taxtotal = taxtotal + item.taxAmount
            disctotal = disctotal + item.discountAmount
        args['ordertotal'] = ordertotal
        args['taxtotal'] = taxtotal
        args['disctotal'] = disctotal


    except:
        messages.error(request,"Sorry! No order with this id found in your account.")
        return redirect("vendor:orders")
    return render(request,"vendor/generateinvoice.html",args)

