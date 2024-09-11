from django.db import models
from django.db.models.signals import pre_save
from module_products.models import Product


# Create your models here.
class TagsModel(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان برچسب")
    slug = models.CharField(max_length=50, blank=True, verbose_name="عنوان آدرس")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    products = models.ManyToManyField(Product, blank=True, verbose_name="محصولات مرتبط به این تگ")

    def __str__(self):
        return self.title

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "برچسب ها"
        verbose_name = "برچسب"


# اینجا برای slug یه تابع مینویسیم و بعدش کانکتش میکنیم
def tags_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance.title.replace(' ', '-')


pre_save.connect(receiver=tags_pre_save, sender=TagsModel)
