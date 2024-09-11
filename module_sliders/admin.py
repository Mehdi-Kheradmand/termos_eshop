from django.contrib import admin
from .models import Slider_model


class Admin_Slider_model(admin.ModelAdmin):

    list_display = ['__str__', 'image', 'active']

    class Meta:
        model = Slider_model


admin.site.register(Slider_model, Admin_Slider_model)
