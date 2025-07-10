from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [    
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Logout,name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('resendactivationemail/',views.ResendActivationEmail.as_view(),name='resendactivationemail'),   
    path('activate/<uidb64>/<token>/',views.ActivateAccount.as_view(),name="activateaccount"),
    path('resetpassword/',views.ResetPassword.as_view(),name='resetpassword'),
    path('createnewpassword/<uidb64>/<token>/',views.CreateNewPassword.as_view(),name="createnewpassword"),  

    path('profile/',views.Profile,name='profile'),
    path('profiledetails/',views.ProfileDetails.as_view(),name='profiledetails'),
    path('changepassword/',views.ChangePassword.as_view(),name='changepassword'),    
    path('address/',views.Address.as_view(),name='address'),        
    path('bankdetails/',views.BankDetails.as_view(),name='bankdetails'),        
    path('dashboard/',views.Dashboard,name='dashboard'),

    path('orders/',views.Orders,name='orders'),
    path('printinvoice/<str:orderid>/',views.PrintInvoice,name='printinvoice'),
    path('generateinvoice/<str:orderid>/',views.GenerateInvoice,name='generateinvoice'),
]
