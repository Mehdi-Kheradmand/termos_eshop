from django.urls import path
from .views import contact_view

urlpatterns = [
    path('', contact_view, name="urls_contact-us_view"),
]

app_name = "module_contact-us"
