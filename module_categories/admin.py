from django.contrib import admin
from .models import ProductCategories, Product_SubCategories


class categories_admin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'slug']

    class Meta:
        model = ProductCategories


class Sub_categories_admin(admin.ModelAdmin):
    list_display = ['title', 'category', 'slug']

    class Meta:
        model = Product_SubCategories


# Register your models here.
admin.site.register(ProductCategories, categories_admin)
admin.site.register(Product_SubCategories, Sub_categories_admin)
