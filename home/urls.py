from django.urls import path
from . import views

urlpatterns = [    
    path('',views.index,name='home'),  
    path('cartsummary/',views.cartsummary,name='cartsummary'),
    path('makepayment/',views.MakePayment,name='makepayment'),
    path('category/<str:cid>/',views.FilterByCategory,name='category'),
    path('allproducts/',views.AllProducts,name='allproducts'),
    path('search/',views.SearchResults,name='search'),

    path('filterproduct',views.FilterProducts,name='filterproduct'),
    path('clearfilter/',views.ClearFilter,name='clearfilter'),
    path('clearfilter/<str:category>/',views.ClearFilter,name='clearfilter'),
    path('pinproducts/',views.FilterByPin,name="pinproducts"), 

    path('aboutus/',views.AboutUs,name='aboutus'),
    path('affiliate/',views.Affiliate,name='affiliate'),
    path('cancellations/',views.Cancellations,name='cancellations'),
    path('careers/',views.Careers,name='careers'),
    path('contactus/',views.ContactUs,name='contactus'),
    path('faqs/',views.FAQ,name='faqs'),
    path('help/',views.Help,name='help'),
    path('payments/',views.Payments,name='payments'),
    path('payouts/',views.Payouts,name='payouts'),
    path('press/',views.Press,name='press'),
    path('howtocare/', views.Howtocare,name='howtocare'),
    path('privacypolicy/',views.PrivacyPolicy,name='privacypolicy'),
    path('refundpolicy/',views.RefundPolicy,name='refundpolicy'),
    path('returnpolicy/',views.ReturnPolicy,name='returnpolicy'),
    path('shippingpolicy/',views.ShippingPolicy,name='shippingpolicy'),
    path('terms/',views.TermsAndConditions,name='terms'),
    path('vendorfaqs/',views.VendorFAQ,name='vendorfaqs'),
    path('vendorassistance/',views.VendorHelp,name='vendorassistance'),
    path('requestproduct/',views.RequestProduct,name='requestproduct'),   
    #path('404/',views.PageNotFound,name='404'),
    #path('404/',views.ServerUnavailable,name='503'),
    path("test-session/", views.test_session)

    
]
