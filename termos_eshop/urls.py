"""
termos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_page, about_us_view, terms_view, sys_view, admin_links

# to use assets
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name="urls_Home_Page"),
    path('about-us', about_us_view, name="urls_about_us"),
    path('terms-conditions', terms_view, name="urls_terms"),
    # path('', AjaxHandlerView.as_view(), name="urls_Home_Page"),
    path('user/', include("module_users.urls", namespace="module_users")),
    path('products/', include("module_products.urls", namespace="module_products")),
    path('orders/', include("module_orders.urls", namespace="module_orders")),
    path('profile/', include("module_profile.urls", namespace="module_profile")),
    path('product_comments/', include("module_product_comments.urls", namespace="product_comments")),
    path('contact-us/', include("module_contact.urls", namespace="module_contact-us")),


    path('sys', sys_view, name="urls_sys"),


    path('termos_admin_panel/', admin.site.urls),
    path('edit_product/<p_id>', admin_links, name="admin_product_editor"),
]


if settings.DEBUG:
    # add root static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
