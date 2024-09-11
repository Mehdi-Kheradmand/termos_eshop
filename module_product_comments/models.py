from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from module_products.models import Product


class Product_Comments_Model(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول مربوطه")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    msg = models.TextField(verbose_name="متن نظر")
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت نظر', auto_now=True)
    is_accepted = models.BooleanField(default=False, verbose_name='تایید شده/نشده')

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "نظرات"
        verbose_name = "نظر"

    def __str__(self):
        return self.product.title
