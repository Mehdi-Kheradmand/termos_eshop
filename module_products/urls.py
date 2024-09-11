from django.urls import path
from .views import ProductsCategoriesView, product_detail_view, Products_SearchAndTag_View, ajax_wishlist

urlpatterns = [
    path('search', Products_SearchAndTag_View.as_view(), name="urls_products_search_tag"),
    path('<main_category>', Products_SearchAndTag_View.as_view(), name="urls_products_list"),
    path('<main_category>/<sub_category>', Products_SearchAndTag_View.as_view(), name="urls_product_list_sub_category"),

    # path('<main_category>', Products_Categories_View.as_view(), name="urls_products_list"),
    # path('<main_category>/<sub_category>', Products_Categories_View.as_view(), name="urls_product_list_sub_category"),

    path('detail/<p_id>/<slug>', product_detail_view, name="urls_product_detail"),

    path('ajax/wishlist_add_remove/', ajax_wishlist, name="urls_ajax_wishlist"),

    path('', ProductsCategoriesView.as_view(), name="urls_products_list_filter"),

]


app_name = "module_products"
