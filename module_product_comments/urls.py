from django.urls import path
from .views import ajax_product_comments

urlpatterns = [
    path('ajax/', ajax_product_comments, name="urls_profile_view"),
]


app_name = "module_product_comments"
