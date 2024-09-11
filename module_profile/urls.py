from django.urls import path
from .views import profile_view, profile_address_edit, \
    profile_address_edit_ajax_view, orders_list_view, order_detail, wishlist_view, edit_profile_view, seller_main_view

urlpatterns = [
    path('dashboard', profile_view, name="urls_profile_view"),

    path('address_edit/', profile_address_edit, name="urls_profile_address_edit"),
    path('address_edit/ajax/', profile_address_edit_ajax_view, name="urls_profile_address_edit_ajax"),

    path('orders_history/', orders_list_view, name="urls_profile_orders_history"),
    path('orders_list/detail/<order_id>', order_detail, name="urls_profile_order_detail"),

    path('wishlist', wishlist_view, name="urls_profile_wishlist"),

    path('edit_profile/', edit_profile_view, name="urls_profile_edit_profile"),

    path('seller/', seller_main_view, name="urls_profile_seller_main"),

]


app_name = "module_profile"
