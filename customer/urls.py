from django.urls import path
from . import views


urlpatterns = [    
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Logout,name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('resendactivationemail/',views.ResendActivationEmail.as_view(),name='resendactivationemail'),   

    # path('activate/<uidb64>/<token>/',views.ActivateAccount.as_view(),name="activateaccount"),
    path('activate/',views.ActivateAccount.as_view(),name="activateaccount"),
    path('resetpassword/',views.ResetPassword.as_view(),name='resetpassword'),
    path('createnewpassword/<uidb64>/<token>/',views.CreateNewPassword.as_view(),name="createnewpassword"),  

    path('profile/',views.Profile.as_view(),name='profile'),
    # path('profiledetails/',views.ProfileDetails.as_view(),name='profiledetails'),
    path('changepassword/',views.ChangePassword.as_view(),name='changepassword'),
    #path('myaddresses/',views.AllAddress,name='myaddresses'),
    path('address/',views.Address.as_view(),name='address'),
    path('address/<int:id>',views.Address.as_view(),name='address'),
    #path('deleteaddress/<int:id>',views.DeleteAddress,name='deleteaddress'),
    #path('setasdefault/<int:id>',views.SetAddressAsDefault,name='setasdefault'),

    path('ordersuccess/',views.OrderPlaced,name='ordersuccess'),
    path('orderfailed/',views.OrderFailed,name='orderfailed'),
    path('ordersuccessful/<str:orderid>',views.OrderSuccess,name='ordersuccessful'),
    path('printinvoice/<str:orderid>/',views.PrintInvoice,name='printinvoice'),
    path('getinvoice/<str:orderid>/',views.GetInvoice,name='getinvoice'),

    path('orders/',views.Orders,name='orders'),
    # path('tracking/<int:oid>/',views.UpdateTrackingInfo,name='tracking'),
    # path('updatestatus/<int:oid>/',views.UpdateOrderStatus,name='updatestatus'),

    path('cancelorder/<int:oid>/',views.CancelOrder,name='cancelorder'),
    path('returnproduct/<int:orderitemid>/',views.ReturnProduct,name='returnproduct'),
]