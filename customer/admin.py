from django.contrib import admin
from customer.models import *


#admin.site.register(Customer)
admin.site.register(UserAddress)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(RazorOrder)
admin.site.register(WishList)
@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","user")


