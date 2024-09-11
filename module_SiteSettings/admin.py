from django.contrib import admin
from .models import site_settings


class settings_admin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'email', 'active']

    class Meta:
        model = site_settings


# Register your models here.
admin.site.register(site_settings, settings_admin)