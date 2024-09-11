from os import path
from django.db import models


def get_file_ext(filepath_and_name):
    # این اسم فایل و پسوندشو از بقیه جدا میکنه مثلا D:/1.jpg رو میگیره فقط 1.jpg رو برمیگردونه
    base_name = path.basename(filepath_and_name)
    # این اسم و پسوند فایل رو جدا میکنه
    name, ext = path.splitext(base_name)
    return name, ext


# logo
def upload_image_path(instance, filename):
    # اسم محصول رو میده اینجا چون پایین __str__ براش تعریف کردیم instance میشه title ولی instance کل مدل محصول میاد توش
    name, ext = get_file_ext(filename)
    return f"images/logo/{instance.site_title.replace(' ','-')}.logo{ext}"


# banner 1
def upload_image_path_banner1(instance, filename):
    # اسم محصول رو میده اینجا چون پایین __str__ براش تعریف کردیم instance میشه title ولی instance کل مدل محصول میاد توش
    name, ext = get_file_ext(filename)
    return f"images/banners/{instance.site_title.replace(' ','-')}.bnr1{ext}"


# banner 2
def upload_image_path_banner2(instance, filename):
    # اسم محصول رو میده اینجا چون پایین __str__ براش تعریف کردیم instance میشه title ولی instance کل مدل محصول میاد توش
    name, ext = get_file_ext(filename)
    return f"images/banners/{instance.site_title.replace(' ','-')}.bnr2{ext}"


# favicon
def upload_image_path_favicon(instance, filename):
    # اسم محصول رو میده اینجا چون پایین __str__ براش تعریف کردیم instance میشه title ولی instance کل مدل محصول میاد توش
    name, ext = get_file_ext(filename)
    return f"images/favicon{ext}"


# Create your models here.
class site_settings(models.Model):
    site_title = models.CharField(max_length=50, default="Welcome, Please edit Site_settings at admin_page", verbose_name="عنوان / نام فروشگاه")
    address = models.TextField(max_length=1000, default="mehdi.kr@gmail.com", verbose_name="آدرس پستی")
    about_us = models.TextField(default="mehdi.kr@gmail.com", verbose_name="درباره فروشگاه")
    phone = models.CharField(default="+989356818853", max_length=15, verbose_name="شماره تماس")
    pre_phone = models.CharField(max_length=4, verbose_name="پیش شماره (مثال : ۰۲۱)", default='021')
    fax = models.CharField(max_length=15, verbose_name="فکس", default="0")
    email = models.EmailField(verbose_name="ایمیل", default="mehdi.kr@gmail.com")
    logo = models.ImageField(upload_to=upload_image_path, blank=True, null=True, default=None, verbose_name="لوگوی فروشگاه")
    index_banner1 = models.ImageField(upload_to=upload_image_path_banner1, blank=True, null=True, default=None, verbose_name="بنر شماره ۱ (428*856)")
    index_banner1_link = models.CharField(max_length=250, verbose_name="لینک بنر شماره ۱", default='/')
    index_banner2 = models.ImageField(upload_to=upload_image_path_banner2, blank=True, null=True, default=None, verbose_name="بنر شماره ۲ (428*856)")
    index_banner2_link = models.CharField(max_length=250, verbose_name="لینک بنر شماره ۲", default='/')
    favicon = models.ImageField(upload_to=upload_image_path_favicon, verbose_name="آیکون وبسایت (ico.)", default='images/favicon.ico')
    transport_limit = models.BooleanField(default=False, verbose_name="امکان ارسال رایگان")
    transport_limit_price = models.CharField(max_length=15, default=500000, verbose_name="حداقل مبلغ خرید برای ارسال رایگان")
    transport_price = models.CharField(max_length=15, default=50000, verbose_name="هزینه حمل و نقل مرسوله")
    is_repairing = models.BooleanField(default=False, verbose_name="حالت تعمیر")
    active = models.BooleanField(default=False, unique=True, verbose_name="فعال/غیرفعال")

    def get_transport_limit_price_with_comma(self):
        numbers = "{:,}".format(int(self.transport_limit_price))
        return numbers

    def get_transport_price_with_comma(self):
        numbers = "{:,}".format(int(self.transport_price))
        return numbers

    def get_transport_limit_price(self):
        return int(self.transport_limit_price)

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "مدیریت تنظیمات وبسایت"
        verbose_name = "ثبت/ویرایش تنظیمات"

    def __str__(self):
        return self.site_title
