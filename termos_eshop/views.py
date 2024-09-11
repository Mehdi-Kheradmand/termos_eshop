# from random import randint
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.clickjacking import xframe_options_exempt
from module_SiteSettings.models import site_settings
from .Utilities import EshopSessions, get_site_settings, giveme_cart
from module_orders.models import Order_Main_Model, Order_Detail_Model
from module_sliders.models import Slider_model
from module_products.models import Product
from module_categories.models import ProductCategories
import locale
import sys
from hashlib import sha256


@xframe_options_exempt
def home_page(req):
    settings = site_settings.objects.first()
    main_cart = giveme_cart(req)
    sliders = Slider_model.objects.filter(active=True)

    # ------- List Slides -------

    # Last Products
    last_products = Product.objects.filter(active=True).order_by('-added_date')

    # cat_1_Slider
    cat_1_slider = ProductCategories.objects.filter(slug='elements')
    if cat_1_slider.count() > 0:
        cat_1_slider = cat_1_slider.first()
    else:
        cat_1_slider = None

    # cat_2_Slider
    cat_2_slider = ProductCategories.objects.filter(slug='Gas-appliance-parts')
    if cat_2_slider.count() > 0:
        cat_2_slider = cat_2_slider.first()
    else:
        cat_2_slider = None

    cont = {
        'site_settings': settings,
        'main_order_cart': main_cart,
        'sliders': sliders,
        'last_products': last_products,
        'category_slider_1': cat_1_slider,
        'category_slider_2': cat_2_slider,
    }

    return render(req, "index.html", cont)


def about_us_view(req):  # 11/11/2022 m/d/y
    return render(req, "AboutUs.html")


def terms_view(req):  # 12/11/22 m/d/y
    return render(req, "TermsConditions.html")


def partial_header_view(req):
    cont = {'site_settings': get_site_settings()}
    return render(req, "shared/_HeaderLayout.html", cont)


def partial_top_bar_categories_view(req):  # 11/11/2022 m/d/y
    cont = {'category_bar': ProductCategories.objects.all()}
    return render(request=req, template_name="shared/_TopBarCategories_Partial.html", context=cont)


def partial_side_bar_categories_view(req):  # 11/11/2022 m/d/y
    cont = {'category_bar': ProductCategories.objects.all()}
    return render(request=req, template_name="shared/_SideBarCategories_Partial.html", context=cont)


def partial_sidebar_cart_view(req, *args, **kwargs):
    main_order_cart = giveme_cart(req)

    if req.user.is_authenticated:

        cont = {'main_order_cart': main_order_cart}

        if kwargs.get("render_to_str"):
            return render_to_string(template_name="shared/_SidebarCart_Partial.html", context=cont, request=req)
        return render(req, "shared/_SidebarCart_Partial.html", cont)

        # -----------------------------
    else:  # User is not Logged in
        # -----------------------------

        cont = {'session_cart_items': main_order_cart}
        if kwargs.get("render_to_str"):
            return render_to_string(template_name="shared/_SidebarCart_Partial.html", context=cont, request=req)
        return render(request=req, template_name="shared/_SidebarCart_Partial.html", context=cont)


def partial_sidebar_cart_button_view(req):
    if req.user.is_authenticated:
        main_order_cart = Order_Main_Model.objects.filter(is_paid=False, owner_id=req.user.id)
        if main_order_cart.count() > 0:
            cont = {'main_order_cart': main_order_cart.first()}
        else:
            cont = {'main_order_cart': main_order_cart}
        return render(req, "shared/_SidebarCartButton_Partial.html", cont)

        # -----------------------------
    else:  # User is not Logged in
        # -----------------------------

        cont = {'main_order_cart': None, 'session_cart_items': EshopSessions(req)}
        return render(request=req, template_name="shared/_SidebarCartButton_Partial.html", context=cont)


def partial_title_icon_view(req):  # Load Icon And title Page
    cont = {'site_settings': get_site_settings()}
    return render(request=req, template_name="shared/_PageTitleIcon_Partial.html", context=cont)


def partial_footer_view(req):
    s_settings = get_site_settings()
    cont = {'site_settings': s_settings}
    return render(req, "shared/_FooterLayout.html", cont)


def admin_links(req, p_id):
    return redirect(to=f"/termos_admin_panel/module_products/product/{ p_id }/change/")


def sys_view(req):
    # phone_verify_num = sha256(str(randint(10000, 99999)).encode()).hexdigest()

    loc_info = "getlocale: " + str(locale.getlocale()) + \
               "<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
               "<br/>file system encoding: " + str(sys.getfilesystemencoding()) + \
               "<br/>sys default encoding: " + str(sys.getdefaultencoding()) + \
               "<br/>sys default encoding: " + str(sys.getdefaultencoding())

    # main_order_cart = Order_Main_Model.objects.filter(owner_id=req.user.id, is_paid=False).first()
    # email_success_payout(req=req, main_order_cart=main_order_cart, send_to="mehdi.kheradmand5@gmail.com")

    # hash
    hashed_str = sha256("kheradmand".encode())
    print(f"hash code is : {hashed_str.hexdigest()}")

    # 33ba10afd4704fa9c6f1184e82c656c7a21d8285824ee237bd812f1f8b325f5a

    hashed_str = sha256("0918723298777kheradmand".encode())
    print(f"hash code is : {hashed_str.hexdigest()}")

    # Get a session value by its key (e.g. 'my_car'), raising a KeyError if the key is not present
    # my_car = req.session['my_car']

    # Get a session value, setting a default if it is not present ('mini')
    # ses = req.session
    # req.session['mayti'] = 'kir koloft'
    # req.session['my_car'] = 'saina'
    # req.session['mayti2'] = '222222'

    # session_cart_items = session_get_cart_items(req)

    # ses = req.session
    main_cart = Order_Main_Model.objects.filter(owner_id=req.user.id, is_paid=False)
    if main_cart.count() == 1:
        main_cart = main_cart.first()
        detail_carts = Order_Detail_Model.objects.filter(from_Main_order=main_cart,
                                                         from_Main_order__owner_id=req.user.id)
        cart_items = {}
        for detail_cart in detail_carts:
            cart_items[detail_cart.id] = detail_cart.count
        req.session['cart_items'] = cart_items
    print(req.session.get('cart_items'))

    # Set a session value

    # Delete a session value
    # del req.session['my_car']

    # return HttpResponse(loc_info)
    return HttpResponse(loc_info)
    # return module_phone_email_verify.views.phone_email_verify_view_main_layout(req)
