from django.db import models


# Create your models here.
class Slider_model(models.Model):
    image = models.ImageField(verbose_name='تصویر اسلایدر (۸۹۰ * ۱۷۸۰)')
    url_link = models.CharField(verbose_name='آدرس لینک', max_length=250)
    active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "اسلایدر"
        verbose_name = "اسلاید"

    def __str__(self):
        return self.image.url
