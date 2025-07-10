from datetime import datetime, timedelta
from django.template import Library
from customer.models import Customer, OrderItems

from product.models import Coupon, Product, ProductMedia, ProductRating, Category

register = Library()

@register.filter("hyphenurl")
def hyphenurl(text):
    text = text.replace("-"," ")
    return text

@register.filter("primaryimage")
def primaryimage(product):
    productimage = ProductMedia.objects.get(product_id=product.id,mainimage=True).productmedia
    return productimage

@register.filter("primaryimageX")
def primaryimage(product):
    productimage = ProductMedia.objects.filter(product_id=product.id).first().productmedia
    return productimage.url

@register.filter("alreadyreviewed")
def alreadyreviewed(product,request):   
    orderitems=OrderItems.objects.filter(productId=product.id,userId=request.user.Customer.id).first()
    rating = ProductRating.objects.filter(user=request.user.Customer.id).first()
    if orderitems is None and rating is None:
        return False
    else:
        return True


@register.filter("getusername")
def primaryimage(user):
    username = Customer.objects.get(id=user).user.fullName
    return username

@register.filter("avgrating")
def primaryimage(product):
    rating = ProductRating.objects.filter(product=product,is_live=True)
    avgrating = 0
    for r in rating:
        avgrating = avgrating + r.rating
    if rating.count() == 0:
        return 0
    else:
        return avgrating / rating.count()
        
@register.filter("cartquantity")
def cartquantity(productid,request):
    cart = request.session.get("cart")
    cartitem= cart.get(str(productid))
    return cartitem["quantity"]


@register.filter("producttotal")
def producttotal(productid,request):
    cart = request.session.get("cart")
    prod = Product.objects.get(id=productid).productSalePrice
    return prod * float(cart.get(str(productid)))


@register.filter("cartvalue")
def cartvalue(request):
    request.session.flush()
    total = 0
    cart = request.session.get("cart")
    if not cart is None:
        for k in cart.keys():
            cartitem = cart[str(k)]
            quantity = int(cartitem["quantity"])
            total = total + Product.objects.get(id=int(k)).productSalePrice * quantity    
    return total

@register.filter("discountamt")
def discountamt(request):  
    discount = 0   
    try:
        discount = request.session.get('discount')
        discount = float(discount)
        return discount
    except:
        return 0

@register.filter("finaltotal")
def finaltotal(request):
    total = 0
    cart = request.session.get("cart")
    for k in cart.keys():
        total = total + Product.objects.get(id=int(k)).productSalePrice * int(cart[str(k)])
    discount = discountamt(request)
    return total - discount


@register.filter("TaxAmt")
def taxpercent(products, request): 
    taxamt= 0
    cart = request.session.get("cart")
    coupon = request.session.get("couponcode")
    if coupon is None:
        for prod in products:
            if prod.taxPercent == 0 or prod.taxPercent == None:
                taxamt = taxamt 
            else:
                taxamt = taxamt + (prod.productSalePrice * (prod.taxPercent/100)  *  int(cart[str(prod.id)]))
        return taxamt
    else:
        coupon = Coupon.objects.get(couponCode=coupon)
        totalcartprice = 0
        for product in products:
            totalcartprice = totalcartprice + (product.productSalePrice * int(cart[str(product.id)]))
        if (totalcartprice * coupon.valueInPercent/100) >= coupon.maxDiscount:
            discount = coupon.maxDiscount
            totalunits = 0
            for key in cart.keys():
                totalunits = totalunits + int(cart[key])
            discount = discount/totalunits
            taxamt = 0
            for prod in products:
                if prod.taxPercent == 0 or prod.taxPercent == None:
                    taxamt = taxamt
                else:                
                    taxamt = taxamt + (prod.productSalePrice - discount)* int(cart[str(prod.id)]) / ((100 + prod.taxPercent) / prod.taxPercent) 
        else:            
            taxamt = 0
            for prod in products:
                taxamt = taxamt + ((prod.productSalePrice - (prod.productSalePrice * coupon.valueInPercent/100))* int(cart[str(prod.id)])) / ((100 + prod.taxPercent) / prod.taxPercent) 
    request.session["tax"] = taxamt
    return taxamt

@register.filter("carttotal")
def CartTotal(request):
    total = 0
    cart = request.session.get("cart")
    for k in cart.keys():
        total = total + Product.objects.get(id=int(k)).productSalePrice * int(cart[str(k)])
    
    return total - discountamt(request)

@register.filter("Tax")
def Tax(product, request): 
    taxamt= 0
    cart = request.session.get("cart")
    coupon = request.session.get("couponcode")
    if coupon is None:        
            taxamt = taxamt + (product.productSalePrice * product.taxPercent / 100) *  int(cart[str(product.id)])    
            return taxamt
    else:
        coupon = Coupon.objects.get(couponCode=coupon)
        totalcartprice = 0        
        for key in cart.keys():
            prod = Product.objects.get(id=key)
            totalcartprice = totalcartprice + (prod.productSalePrice * int(cart[str(prod.id)]))
        if (totalcartprice * coupon.valueInPercent/100) >= coupon.maxDiscount:
            discount = coupon.maxDiscount
            totalunits = 0
            for key in cart.keys():
                totalunits = totalunits + int(cart[key])
            discount = discount/totalunits           
            taxamt = (product.productSalePrice - discount)* int(cart[str(product.id)]) * product.taxPercent/100
        else:                    
            taxamt = ((product.productSalePrice - (product.productSalePrice * coupon.valueInPercent/100))* int(cart[str(product.id)])) * product.taxPercent/100
    return round(taxamt,2)


@register.filter("cartproducttotal")
def CartTotal(product,request):    
    cart = request.session.get("cart")    
    coupon = request.session.get("couponcode")
    if coupon is None:
        for key in cart.keys():
            product = Product.objects.get(id=key)
            carttotal = product.productSalePrice *  int(cart[str(product.id)])    
        return carttotal
    else:
        coupon = Coupon.objects.get(couponCode=coupon)
        totalcartprice = 0
        for key in cart.keys():
            prod = Product.objects.get(id=key)
            totalcartprice = totalcartprice + (prod.productSalePrice * int(cart[str(prod.id)]))
        if (totalcartprice * coupon.valueInPercent/100) >= coupon.maxDiscount:
            discount = coupon.maxDiscount
            totalunits = 0
            for key in cart.keys():
                totalunits = totalunits + int(cart[key])
            discount = discount/totalunits                                    
            return (product.productSalePrice - discount) *  int(cart[str(product.id)])
        else:                                    
            return ((product.productSalePrice - (product.productSalePrice * coupon.valueInPercent/100))* int(cart[str(product.id)]))


@register.filter("returnvalid")
def returnvalid(deliverydate):
    if datetime.today().date() <= deliverydate + timedelta(days=15):
        return True
    else:
        return False

@register.filter("containspin")
def containspin(request):
    pin = request.session.get('pincode')
    if pin is None or pin == '':
        return False
    else:
        return True
    
    
@register.filter("pinvalue")
def pinvalue(request):
    pin = request.session.get('pincode')
    if pin is None or pin == '':
        return False
    else:
        return pin
    

@register.filter("reviewsCount")
def reviewsCount(product):
    rating = ProductRating.objects.filter(product=product,is_live=True)
    if rating is None:
        return "0 Reviews"    
    return str(rating.count()) + " Reviews"

@register.filter("allcategories")
def allcategories(request):
    allcategories = Category.objects.all()
    return allcategories

@register.filter("pagetitle")
def pagetitle(request):
    if "contact" in request.path.lower():
        return "Contact Us"
    elif "about" in request.path.lower():
        return "About Us"
    elif "terms" in request.path.lower():
        return "Terms and Conditions"
    elif "privacy" in request.path.lower():
        return "Privacy Policy"
    elif "faq" in request.path.lower():
        return "FAQs"
    elif "login" in request.path.lower():
        return "Login"
    elif "register" in request.path.lower():
        return "Register"
    elif "change" in request.path.lower():
        return "Change Password"
    elif "profile" in request.path.lower():
        return "Profile"
    elif "cancellations" in request.path.lower():
        return "Cancellations"
    elif "return" in request.path.lower():
        return "Return Policy"
    elif "refund" in request.path.lower():
        return "Refund Policy"
    elif "affiliate" in request.path.lower():
        return "Affiliate"
    elif "career" in request.path.lower():
        return "Careers"
    elif "plants" in request.path.lower():
        return "Plants"
    elif "pots" in request.path.lower():
        return "Pots"
    elif "fertilizers" in request.path.lower():
        return "Fertilizers"
    elif "flowers" in request.path.lower():
        return "Flowers"
    


@register.filter("characters")
def characters(textphrase):    
    return textphrase[:150]


@register.filter("cartproducts")
def cartproducts(request):    
    # request.session.flush()
    cart = request.session.get("cart")
    if cart is None:    
        cart={}
        request.session["cart"] = cart  
    cart = request.session.get("cart")
    products = Product.objects.filter(id__in=cart.keys()) 
    return products

@register.filter("selectedcategory")
def selectedcategory(products, category):    
    return products.filter(category=category)


@register.filter("productsincategory")
def productsincategory(category):    
    products = Product.objects.filter(category__categoryName=category).count()
    return products

@register.filter("MRPdiscount")
def MRPdiscount(product):    
    res =  int((1 - (float(product.productSalePrice) / float(product.productMRP)))* 100)
    return "-" + str(res) + "%"
    

