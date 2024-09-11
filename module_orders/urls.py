from django.urls import path
from .views import orders_cart_view, ajax_delete_from_cart, ajax_delete_from_sidebar, ajax_change_amount, checkout_view, ajax_add_to_cart
from .payment_verify_views import verify_payment_view

urlpatterns = [
    path('cart', orders_cart_view, name="urls_cart"),

    # ajax_delete from cart page
    path('cart/ajax/c-delete/', ajax_delete_from_cart, name="urls_ajax_delete_cart_page_item"),

    # ajax_delete from sidebar cart
    path('cart/ajax/s-delete/', ajax_delete_from_sidebar, name="urls_ajax_delete_side_cart_item"),

    path('cart/json/amount/', ajax_change_amount, name="urls_ajax_change_amount"),

    path('checkout/', checkout_view, name="urls_checkout"),
    path('checkout/<repay_cart_id>', checkout_view, name="urls_checkout_repay"),

    path('verify/', verify_payment_view, name="urls_verify_payment"),
    path('verify/<cart_id>', verify_payment_view, name="urls_verify_payment_callback"),


    path('ajax/add_to_cart/', ajax_add_to_cart, name="urls_ajax_add_to_cart"),
]


app_name = "module_orders"
