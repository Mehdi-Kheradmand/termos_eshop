from django.contrib import admin
from .models import Product, ProductsGallery


class product_admin(admin.ModelAdmin):
    list_display = ['__str__', 'stock', 'price', 'main_big_image', 'active', 'visit_counter']
    readonly_fields = ['visit_counter', 'added_date']

    class Meta:
        model = Product


class product_admin_gallery(admin.ModelAdmin):
    list_display = ['__str__', 'big_image', 'small_image']

    class Meta:
        model = ProductsGallery


# Register your models here.
admin.site.register(Product, product_admin)
admin.site.register(ProductsGallery, product_admin_gallery)
