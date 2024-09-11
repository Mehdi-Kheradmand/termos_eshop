from django.contrib import admin
from .models import UserAdditional, UserAddress
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# show one-to-one table in User admin panel (show useradditional in User's  admin panel)


# create a class inherited from admin.StackedInline
class UserAdditionalInline(admin.StackedInline):
    model = UserAdditional
    can_delete = False
    verbose_name_plural = 'سایر مشخصات'


# حالا اون کلاسی که بالا ساختیم رو به admin اضافه میکنیم
# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserAdditionalInline,)


# اینم که ربطی به داستان اصلی نداره میخوایم مدل آدرس هم توی کل ادمین داشته باشیم
class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'state', 'city', 'address_detail']

    class Meta:
        model = UserAddress


# حالا اول شکل قبلی رو پاک میکنیم و جدیده رو ریجیستر میکنیم
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# مدل آدرس ها هم به کل ادمین اضافه میکنیم مثل قبلا
admin.site.register(UserAddress, AddressAdmin)
