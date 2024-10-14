import os
import random
from django.contrib.auth.models import User
from django.db import models
from .model_managers import ProductManager
from module_categories.models import ProductCategories, Product_SubCategories


def is_it_numeric(txt):
    if txt is None or txt == '':
        return False
    if type(txt) is int:
        return True
    for char in txt:
        if not char.isdigit():
            return False
    return True


def give_me_the_product_by_id(p_id):
    if not is_it_numeric(p_id):
        return None
    the_product = Product.objects.filter(id=p_id, active=True)
    if the_product.count() != 0:
        return the_product.first()
    return None


def get_file_ext(filepath_and_name):
    base_name = os.path.basename(filepath_and_name)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_file_ext(filename)
    return f"images/products/{instance.title.replace(' ', '-')}/{instance.title}{ext}"


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    price = models.DecimalField(decimal_places=0, max_digits=12, verbose_name="قیمت (تومان)")
    description = models.TextField(verbose_name="توضیحات")
    main_big_image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر اصلی محصول (سایز بزرگ)",
                                       null=True)
    main_small_image = models.ImageField(upload_to=upload_image_path,
                                         verbose_name="تصویر اصلی محصول(سایز کوچک ۱۸۵*۱۸۵)", null=True)
    active = models.BooleanField(verbose_name="فعال/غیرفعال")
    stock = models.IntegerField(verbose_name="موجودی")
    added_date = models.DateTimeField(auto_created=True, auto_now_add=True,
                                      verbose_name="زمان اضافه شدن محصول به وبسایت")
    visit_counter = models.IntegerField(verbose_name="تعداد بازدید محصول", default=0)

    categories = models.ManyToManyField(ProductCategories, blank=True, verbose_name="دسته بندی های اصلی")
    sub_categories = models.ManyToManyField(Product_SubCategories, blank=True, verbose_name="دسته بندی های فرعی")
    wisher_users = models.ManyToManyField(User, verbose_name="موجود در لیست علاقه مندی", blank=True)

    seller = models.ForeignKey(User, verbose_name="فروشنده محصول", null=True, blank=True, on_delete=models.CASCADE,
                               related_name="product_seller")
    incoming_price = models.DecimalField(decimal_places=0, max_digits=12, default=0, blank=True, null=True,
                                         verbose_name="قیمت خرید فروشنده(تومان)")
    auto_price_update = models.BooleanField(verbose_name="تایین قیمت خودکار", default=False)
    price_percent = models.DecimalField(decimal_places=0, max_digits=3, default=0, verbose_name="ضریب افزایش قیمت")

    # categories =

    objects = ProductManager()

    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"

    def __str__(self):
        return self.title

    # for address_bar showing
    def get_url_bar(self):
        return f"detail/{self.id}/{self.title.replace(' ', '-')}"

    def get_slug(self):
        return self.title.replace(' ', '-')

    def get_category_name(self):
        return self.categories.name

    def split_description(self):
        response = self.description.split('\r\n')
        return response

    def get_price_with_comma(self):
        return "{:,}".format(int(self.price))

    def get_incoming_price_with_comma(self):
        return "{:,}".format(int(self.incoming_price))

    # def get_amount_in_session(self):
    #     cart_items = EshopSessions.__new__(EshopSessions)
    #     return cart_items.get_amount_of_product_in_cart(the_product=give_me_the_product_by_id(self.id))


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------- PRODUCTS GALLERY CLASS
# ------------------------------------------------------------------------------------------------------


def upload_image_gallery(instance, filename):
    name, ext = get_file_ext(filename)
    rand = random.randint(1000, 9999)
    title = instance.product.title
    final = f"images/products/{title.replace(' ', '-')}/{title}{rand}{ext}"
    return final


class ProductsGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول مربوطه")
    big_image = models.ImageField(upload_to=upload_image_gallery, verbose_name="تصویر بزرگ")
    small_image = models.ImageField(upload_to=upload_image_gallery, verbose_name="تصویر کوچک ۱۸۵*۱۸۵")

    class Meta:
        verbose_name_plural = "گالری تصاویر"
        verbose_name = "تصویر محصول"

    def __str__(self):
        return self.product.title
