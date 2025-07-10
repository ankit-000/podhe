from django.contrib import admin
from .models import *

admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(ProductMedia)
admin.site.register(ProductRating)
admin.site.register(ProductRatingMedia)
admin.site.register(Coupon)

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ("productName","category","productMRP","productSalePrice","is_live","is_visible",'addedOn')

@admin.register(ProductMedia)
class UserAdmin(admin.ModelAdmin):
    list_display = ("productmedia","product","mainimage")
    ordering = ["product"]
