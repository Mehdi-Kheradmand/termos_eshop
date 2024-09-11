from django.contrib import admin
from .models import Order_Main_Model, Order_Detail_Model


class Admin_Order_Main_Model(admin.ModelAdmin):

    list_display = ['__str__', 'is_paid', 'payment_date', 'owner', 'payment_status']

    class Meta:
        model = Order_Main_Model


class Admin_Order_Detail_Model(admin.ModelAdmin):

    list_display = ['__str__', 'from_Main_order', 'product', 'price', 'count']

    class Meta:
        model = Order_Detail_Model


admin.site.register(Order_Main_Model, Admin_Order_Main_Model)
admin.site.register(Order_Detail_Model, Admin_Order_Detail_Model)
