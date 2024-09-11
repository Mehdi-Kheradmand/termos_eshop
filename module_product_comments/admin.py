from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product_Comments_Model


class Admin_Product_Comments(admin.ModelAdmin):

    list_display = ['__str__', 'owner', 'created_date', 'msg', 'is_accepted']

    class Meta:
        model = Product_Comments_Model


admin.site.register(Product_Comments_Model, Admin_Product_Comments)

