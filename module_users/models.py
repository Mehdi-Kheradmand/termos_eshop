from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import pre_save


# Regex for mobile Phone
# phone_number = forms.CharField(label='شماره موبایل', max_length=11, validators=[RegexValidator(regex=r'09(\d{9})$')])

# Create your models here.
class UserAdditional(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر مربوطه")
    Phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="موبایل")
    mellicode = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name="کد ملی")
    phone_verified = models.BooleanField(default=False, verbose_name="تایید موبایل")
    Email_verified = models.BooleanField(default=False, verbose_name="تایید ایمیل")
    last_ip = models.CharField(max_length=12, unique=True, blank=True, null=True, verbose_name="آخرین آدرس آیپی")
    birth_jalali = models.CharField(max_length=10, blank=True, null=True, verbose_name="تاریخ تولد")
    new_phone_to_change = models.CharField(max_length=11, blank=True, null=True, verbose_name="موبایل جدید برای تغییر")

    phone_verify_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد تایید ارسال شده به موبایل")
    phone_verify_hash_code = models.CharField(max_length=256, blank=True, null=True, verbose_name="کد تایید هش موبایل")
    phone_verify_date_code = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ ارسال کد تایید به موبایل")

    email_verify_code = models.CharField(max_length=15, blank=True, null=True, verbose_name="کد تایید ارسال شده به ایمیل")
    email_verify_hash_code = models.CharField(max_length=256, blank=True, null=True, verbose_name="کد تایید هش ایمیل")
    email_verify_date_code = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ ارسال کد تایید به ایمیل")

    IsSeller = models.BooleanField(verbose_name="فروشنده", default=False)

    # joined_jalali =
    # last_login_jalali =

    def cart_count(self):
        return self.Phone

    # to Show in admin panel
    class Meta:
        verbose_name_plural = "سایر مشخصات کاربران"
        verbose_name = "سایر مشخصات کاربر"

    def __str__(self):
        return self.owner.get_full_name()


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر مربوطه")

    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="نام")
    family = models.CharField(max_length=250, blank=True, null=True, verbose_name="نام خانوادگی")
    state = models.CharField(max_length=20, blank=True, null=True, verbose_name="استان")
    city = models.CharField(max_length=20, blank=True, null=True, verbose_name="شهر")
    address_detail = models.CharField(max_length=250, blank=True, null=True, verbose_name="آدرس پستی")
    post_code = models.CharField(max_length=250, blank=True, null=True, verbose_name="کد پستی")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="موبایل")
    email = models.CharField(max_length=50, blank=True, null=True, verbose_name="ایمیل")
    phone_verify_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد تایید ارسال شده به موبایل")
    phone_verify_date_code = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ ارسال کد تایید به موبایل")
    # phone_verify_send_date

    # to Show in admin panel
    class Meta:
        verbose_name_plural = "آدرس کاربران"
        verbose_name = "آدرس کاربر"

    def __str__(self):
        return self.user.get_full_name()


class WishlistModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر مربوطه")

# def user_pre_save(sender, instance, *args, **kwargs):
#     print(f"Sender : {sender}")
#     print(f"Instance : {instance}")
#     print(f"args : {args}")
#     print(f"kwargs : {kwargs}")
#     print(f"instance.title : {instance.title}")
#     # if not instance.title:
#     #     print(f"{product.title} -- {random.randint(1000,9999)}")
#     #     instance.title = f"{ProductGallery.product.objects.} {random.randint(1000,9999)}"
#
#
# pre_save.connect(user_pre_save(), sender=user_additional)
