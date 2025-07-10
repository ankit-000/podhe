from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.Products.as_view(),name="products"), 
    path('addproduct/',views.AddProduct.as_view(),name="addproduct"), 
    path('addproduct/<int:pid>/',views.AddProduct.as_view(),name="addproduct"), 
    path('deleteproduct/<int:pid>/',views.DeleteProduct.as_view(),name="deleteproduct"),  
    path('addmedia/<int:pid>/',views.AddProductMedia.as_view(),name="addmedia"), 
    path('deletemedia/<int:pid>/<int:mid>/',views.DeleteProductMedia.as_view(),name="deletemedia"), 
    path('makeprimary/<int:pid>/<int:mid>/',views.MakePrimary.as_view(),name="makeprimary"), 

    path('details/<int:pid>',views.details.as_view(),name="details"), 
    path('addtocart/',views.AddToCart,name="addtocart"),  
    path('buynow/',views.BuyNow,name="buynow"),       
    path('updatecart/<int:pid>/',views.UpdateCart,name="updatecart"),     
    path('removefromcart/<int:pid>',views.RemoveFromCart,name="removefromcart"),     
    path('addtowishlist/<int:pid>',views.AddToWishlist,name="addtowishlist"),     
    path('wishlist/',views.Wishlist,name="wishlist"),     
    path('removefromwishlist/<int:pid>/',views.RemoveFromWishList,name="removefromwishlist"),     
    path('addreview/<int:pid>/',views.AddReview.as_view(),name="addreview"), 

    path('applycoupon/',views.ApplyCoupon,name="applycoupon"),   
    path('removecoupon/',views.RemoveCoupon,name="removecoupon"),   
    # path('pinproducts/',views.FilterByPin,name="pinproducts"),  
]

