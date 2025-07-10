from unicodedata import category
from django.shortcuts import redirect, render
from django.db.models.query_utils import Q
from home.models import RequestedProducts
from product.models import Category, Product
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# def index(request):
#     pin = request.session.get('pincode')
#     if pin is None or pin == '':
#         products = Product.objects.filter(is_live=True,category__categoryName='Plants')
#     else:
#         products = Product.objects.filter(is_live=True,addedBy__address__pinCode = pin)
#     categories = Category.objects.all()
#     return render(request,'home/index.html',{"products":products,"categories":categories})

def index(request):
    products = Product.objects.filter(is_live=True)
    categories = Category.objects.all()    
    cart = request.session.get("cart")    
    return render(request,'home/index.html',{"products":products,"categories":categories})


def FilterByCategory(request,cid):
    category = Category.objects.get(categoryName=cid)
    categories = Category.objects.all()
    # pin = request.session.get('pincode')
    # if pin is None or pin == '':
    products = Product.objects.filter(category=category,is_live=True)
    # else:
    #     products = Product.objects.filter(category=category,is_live=True,addedBy__address__pinCode = pin)
    paginator = Paginator(products, 5)  # Show 25 contacts per page.    

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'home/categories.html',{"category":category,"page_obj":page_obj,"categories":categories,"categoryid":cid})

def AllProducts(request):    
    products = Product.objects.filter(is_live=True)
    paginator = Paginator(products, 5)  # Show 25 contacts per page.
    categories = Category.objects.all()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    #return render(request, "list.html", {"page_obj": page_obj})
    return render(request,'home/categories.html',{"page_obj":page_obj,"categories":categories})


def SearchResults(request):
    query = request.GET['search']
    pin = request.session.get('pincode')
    if pin is None or pin == '':
        products = Product.objects.filter(Q(tagCloud__icontains=query) | Q(productName__icontains=query)| Q(productDescription__icontains=query))
    else:
        products = Product.objects.filter(Q(tagCloud__icontains=query) | Q(productName__icontains=query)| Q(productDescription__icontains=query),addedBy__address__pinCode = pin)  

    paginator = Paginator(products, 5)  # Show 25 contacts per page.    

    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)
    return render(request,'home/searchresults.html',{"products":products,"page_obj":page_obj,"query":query})
    #return render(request, "home/searchresults.html",{"products":products,"query":query})



def FilterProducts(request):
    
    minprice = request.GET["minprice"]
    maxprice = request.GET["maxprice"]
    planttype = request.GET["planttype"]
    productsize = request.GET["productsize"]
    category = request.GET['category']  
    search=request.GET['query']
    sortby = request.GET['sorting']

    





    if minprice == "":
        minprice = 0    
    if maxprice =="":
        maxprice=99999

    if category != "":
        selcategory = Category.objects.filter(categoryName=category).first()
        products = Product.objects.filter(productSalePrice__gte=minprice, productSalePrice__lte=maxprice, category=selcategory)
    elif search != "":
        products = Product.objects.filter(Q(tagcloud__contains=search) | Q(productName__contains=search)| Q(productDescription__contains=search))
        products = products.filter(productSalePrice__gte=minprice, productSalePrice__lte=maxprice)
    else:
        products = Product.objects.filter(productSalePrice__gte=minprice, productSalePrice__lte=maxprice) 

    
    # if pincode != "":
    #     products = products.filter(addedby__User__pincode = pincode)
    
    if planttype !="":
        products = products.filter(tagCloud__contains=planttype)
    
    if productsize != "":
        products = products.filter(size=productsize)

    if sortby == "sortascending":
        products=products.order_by('productSalePrice')
    elif sortby == "sortdescending":
        products=products.order_by('-productSalePrice')
    elif sortby == "newfirst":
        products=products.order_by('-addedOn')
    elif sortby == "oldfirst":
        products=products.order_by('addedOn')   
    elif sortby == "rating":
        products=products.order_by('-productrating__rating')

    pin = request.session.get('pincode')
    if not pin is None and pin != '':
        products=products.filter(addedBy__address__pinCode = pin)

    args = {}
    args['products'] = products
    args['minprice'] = minprice
    args['maxprice'] = maxprice
    # args['pincode'] = pincode
    args['planttype'] = planttype
    args['productsize'] = productsize
    args['categoryid'] = category
    args['query'] = search
    args['sortby'] = sortby

    categories = Category.objects.all()
    args['categories'] = categories


    return render(request,'home/categories.html',args)
    

def ClearFilter(request,category=''):    
    if category == '':
        return redirect('home')
    else:
        url = "{}/{}".format("/category",category)
        return redirect(url)


def FilterByPin(request):
    pin = request.GET["filterpincode"]    
    # products = Product.objects.filter(addedBy__address__pinCode = pin)
    # categories = Category.objects.all()
    request.session["pincode"] = pin
    return redirect("home")




def AboutUs(request):
    categories = Category.objects.all()
    return render(request,"home/aboutus.html",{"categories":categories})

def Careers(request):
    return render(request,"home/careers.html")

def ContactUs(request):
    return render(request,"home/contactus.html")

def FAQ(request):
    return render(request,"home/faqs.html")

def Help(request):
    return render(request,"home/help.html")

def Payments(request):
    return render(request,"home/payments.html")

def Press(request):
    return render(request,"home/press.html")

def PrivacyPolicy(request):
    return render(request,"home/privacypolicy.html")

def RefundPolicy(request):
    return render(request,"home/refundpolicy.html")

def ReturnPolicy(request):
    return render(request,"home/returnpolicy.html")

def ShippingPolicy(request):
    return render(request,"home/shippingpolicy.html")

def TermsAndConditions(request):
    return render(request,"home/termsandconditions.html")

def Cancellations(request):
    return render(request,"home/cancellations.html")


def VendorFAQ(request):
    return render(request,"home/vendorfaqs.html")

def VendorHelp(request):
    return render(request,"home/vendorhelp.html")

def Payouts(request):
    return render(request,"home/payouts.html")

def Affiliate(request):
    return render(request,"home/affiliate.html")

def Howtocare(request):
    return render(request,"home/howtocare.html")


def RequestProduct(request): 

    if request.POST:
        email = request.POST["email"]
        fname = request.POST["fullname"]
        desc= request.POST["requesttext"]
        reqorder = RequestedProducts.objects.create(emailAddress=email,fullName=fname,requestDescription= desc)  
        reqorder.save()
        messages.success(request,"Request Submitted Successfully! We will get back to you soon.")        
    return render(request,"home/requestproduct.html")

def PageNotFound(request):
    return render(request,"404.html")

def ServerUnavailable(request):
    return render(request,"503.html")

from django.http import HttpResponse
    
def test_session(request):
    request.session["test"] = "hello"
    request.session.save()
    return HttpResponse("Session test done!")