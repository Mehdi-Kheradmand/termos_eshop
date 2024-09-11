from django.db import models
from module_users.models import User
from module_products.models import Product
from module_SiteSettings.models import site_settings


def get_site_settings():
    finder = site_settings.objects.filter(active=True)

    if finder.count() == 0:
        finder = site_settings.objects.all()
        if finder.count() == 0:
            new_setting = site_settings.objects.create(active=True)
            new_setting.save()
            return new_setting

    s_settings = finder.first()
    return s_settings


class Order_Main_Model(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="آیدی مالک سبد خرید")
    is_paid = models.BooleanField(verbose_name="پرداخت (شده / نشده)", default=False)
    payment_date = models.DateTimeField(verbose_name="تاریخ پرداخت", null=True)
    payment_status = models.IntegerField(verbose_name="وضعیت پرداخت (۰=موفق ۱=ناموفق ۲=بررسی ۳=لغو شده ۴=مرجوع شده)", default=2)
    package_status = models.IntegerField(verbose_name="وضعیت بسته (۰=جمع آوری ۱=پک شده ۲=ارسال‌شده. مرجوعی: ۰=بررسی ۱=استرداد‌مبلغ ۲=غیر قابل قبول)", default=1)

    # شماره تراکنش و اینا هم میشه بهش اضافه کرد
    transport_price = models.CharField(default=0, max_length=6, verbose_name="هزینه حمل و نقل")
    transaction_id = models.CharField(blank=True, null=True, max_length=100, verbose_name="شناسه پرداخت")
    post_tracking = models.CharField(blank=True, null=True, max_length=150, verbose_name="کد رهگیری مرسوله")
    order_status = models.CharField(blank=True, null=True, max_length=150, verbose_name="کد پیگیری سفارش")
    error_message = models.CharField(blank=True, null=True, max_length=250, verbose_name="پیام درگاه پرداخت")
    cart_notes = models.TextField(blank=True, null=True, verbose_name="توضیحات سفارش")

    receiver_first_name = models.CharField(max_length=120, default='', verbose_name="نام گیرنده")
    receiver_last_name = models.CharField(max_length=120, default='', verbose_name="نام خانوادگی گیرنده")
    receiver_address = models.TextField(verbose_name="آدرس گیرنده", default='')
    receiver_phone = models.CharField(max_length=12, verbose_name="تلفن گیرنده", default=0)
    receiver_email = models.CharField(max_length=50, verbose_name="ایمیل گیرنده", default=0)
    receiver_postalcode = models.CharField(max_length=12, verbose_name="کد پستی", default=0)

    def get_total_price(self):
        # details = Order_Detail_Model.objects.filter(from_Main_order=self)
        details = self.get_order_details().all()
        total_price = 0
        for detail in details:
            total_price += detail.total_price()
        return int(total_price)

    def get_total_price_with_comma(self):
        details = Order_Detail_Model.objects.filter(from_Main_order=self)
        total_price = 0
        for detail in details:
            total_price += detail.total_price()
        return "{:,}".format(total_price)

    def get_total_price_plus_transport(self):
        return self.get_total_price() + self.get_transport_value()

    def get_total_price_plus_transport_with_comma(self):
        return "{:,}".format(self.get_total_price() + self.get_transport_value())

    def get_amount(self):
        details = Order_Detail_Model.objects.filter(from_Main_order=self)
        amount = 0
        for detail in details:
            amount += detail.count
        return amount

    def update_prices(self):
        detail_carts = self.order_detail_model_set.all()
        if not self.is_paid:
            for detail_cart in detail_carts:
                product_price = Product.objects.filter(id=detail_cart.product.id).first().price
                detail_cart.price = product_price
                detail_cart.save()

    def get_transport_value(self):
        return int(self.transport_price)

    def get_transport_value_with_comma(self):
        return "{:,}".format(int(self.transport_price))

    def get_id_plus_1000(self):
        return self.id + 1000

    # you can use "order_main  >> .order_detail_model_set.all()"
    def get_order_details(self):
        order_detail_list = Order_Detail_Model.objects.filter(from_Main_order=self)
        return order_detail_list

    # according to site settings it will return the total_price plus transport price
    def get_final_price_to_pay_with_comma(self):
        s_settings = get_site_settings()
        total_price = self.get_total_price()
        if s_settings.transport_limit:
            if total_price >= int(s_settings.transport_limit_price):
                # free shipping
                return self.get_total_price_with_comma()
        return "{:,}".format(int(s_settings.transport_price) + total_price)

    def get_final_price_to_pay(self):
        s_settings = get_site_settings()
        total_price = self.get_total_price()
        if s_settings.transport_limit:
            if total_price >= int(s_settings.transport_limit_price):
                # free shipping
                return self.get_total_price()
        return int(s_settings.transport_price) + total_price

    def get_amount_of_product_in_cart(self, the_product):
        detail_order = Order_Detail_Model.objects.filter(from_Main_order=self, product=the_product)
        if detail_order.count() == 1:
            detail_order = detail_order.first()
            return detail_order.count
        return 0

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "سبد های خرید کاربران"
        verbose_name = "سبد خرید کاربر"

    # این زیری چه میگه ؟ توی دیتابیس توی پیج ادمین موارد رو با product_object 1 2 3 میبینیم این باعث میشه با title ببینیم
    def __str__(self):
        return self.owner.get_full_name()


class Order_Detail_Model(models.Model):
    from_Main_order = models.ForeignKey(Order_Main_Model, on_delete=models.CASCADE, verbose_name="سبد خرید مربوطه")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.IntegerField(verbose_name="قیمت محصول")
    count = models.IntegerField(verbose_name="تعداد")

    def total_price(self):
        return self.price * int(self.count)

    def total_price_with_comma(self):
        total_price = self.price * int(self.count)
        return "{:,}".format(total_price)

    def get_price_with_comma(self):
        return "{:,}".format(int(self.price))

    # برای نمایش داخل ادمین
    class Meta:
        verbose_name_plural = "محصولات داخل سبد خرید ها"
        verbose_name = "محتوای سبد خرید"

    # این زیری چه میگه ؟ توی دیتابیس توی پیج ادمین موارد رو با product_object 1 2 3 میبینیم این باعث میشه با title ببینیم
    def __str__(self):
        return self.product.title
