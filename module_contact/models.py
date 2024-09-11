from django.db import models


# Create your models here.
class ContactUsForm_Model(models.Model):
    name = models.CharField(max_length=120, verbose_name="نام")
    title = models.CharField(max_length=120, verbose_name="عنوان")
    msg = models.TextField(verbose_name="متن پیام")
    email = models.EmailField(verbose_name="ایمیل")
    seen = models.BooleanField(default=False, verbose_name="خوانده شده/نشده")
    created_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ درج نظر")

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "پیام های کاربران"
        verbose_name = "پیام"

    # این زیری چه میگه ؟ توی دیتابیس توی پیج ادمین موارد رو با product_object 1 2 3 میبینیم این باعث میشه با title ببینیم
    def __str__(self):
        return self.title
