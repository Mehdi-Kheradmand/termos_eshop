import os

from django.db import models


def upload_image_path(instance, filename):
    name, ext = get_file_ext(filename)
    return f"images/categories/{instance.title.replace(' ','-')}/{instance.title}{ext}"


def get_file_ext(filepath_and_name):
    # این اسم فایل و پسوندشو از بقیه جدا میکنه مثلا D:/1.jpg رو میگیره فقط 1.jpg رو برمیگردونه
    base_name = os.path.basename(filepath_and_name)
    # این اسم و پسوند فایل رو جدا میکنه
    name, ext = os.path.splitext(base_name)
    return name, ext


# Create your models here.
class ProductCategories(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.CharField(max_length=100, verbose_name="عنوان در URL")
    banner = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='بنر دسته بندی برای اسلایدر و غیره (اختیاری)')

    def sub_menus(self):
        # sub_result = None
        # for sub_menu in self.product_subcategories_set.all():
        #     sub_result += sub_menu.title
        return self.product_subcategories_set.all()

    def giveme_products(self):
        return self.product_set.filter(active=True)

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"

    # این زیری چه میگه ؟ توی دیتابیس توی پیج ادمین موارد رو با product_object 1 2 3 میبینیم این باعث میشه با title ببینیم
    def __str__(self):
        return self.title


class Product_SubCategories(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, verbose_name="دسته بندی اصلی")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.CharField(max_length=100, verbose_name="عنوان در URL")

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "زیر دسته بندی ها"
        verbose_name = "زیر دسته"

    # این زیری چه میگه ؟ توی دیتابیس توی پیج ادمین موارد رو با product_object 1 2 3 میبینیم این باعث میشه با title ببینیم
    def __str__(self):
        return self.title
