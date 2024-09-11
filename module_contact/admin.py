from django.contrib import admin
from .models import ContactUsForm_Model


class Admin_ContactUsForm_Model(admin.ModelAdmin):

    list_display = ['__str__', 'name', 'email', 'title', 'created_date', 'seen']

    class Meta:
        model = ContactUsForm_Model


admin.site.register(ContactUsForm_Model, Admin_ContactUsForm_Model)
