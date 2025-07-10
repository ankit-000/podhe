from django.contrib import admin

from common.models import User, Invoice

# Register your models here.

# admin.site.register(User)

#admin.site.register(Invoice)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","is_active","is_customer","is_vendor","fullName","gender","contactNumber")

@admin.register(Invoice)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "order","invoiceNo","invoiceDate")
