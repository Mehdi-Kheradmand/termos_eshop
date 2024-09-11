from django.urls import path
from .views import log_out_view
from .views import login_view, ajax_email_phone, ajax_password, ajax_otp, ajax_otp_reset, ajax_register

urlpatterns = [
    path('login/', login_view, name="urls_Login_Page"),
    path('login/email-phone/', ajax_email_phone, name="urls_ajax_email_phone"),

    path('login/ajax_password/', ajax_password, name="urls_ajax_password"),
    path('login/ajax_otp/', ajax_otp, name="urls_ajax_otp"),
    path('login/ajax_otp_reset/', ajax_otp_reset, name="urls_ajax_otp_reset"),  # Do not change (used in layout)
    path('login/ajax_register/', ajax_register, name="urls_ajax_register"),

    path('logout', log_out_view, name="urls_Logout"),
]


app_name = "module_users"
