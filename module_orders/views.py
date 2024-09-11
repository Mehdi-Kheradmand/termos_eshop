import module_users.models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from termos_eshop.views import partial_sidebar_cart_view
from module_SiteSettings.models import site_settings
from module_profile.views import profile_address_edit
from django.urls import reverse
from termos_eshop.Utilities import giveme_cart, \
    create_new_or_update_product_in_cart, give_me_the_product_by_id
from module_orders.models import Order_Main_Model, Order_Detail_Model
from termos_eshop.Utilities import is_ajax, bad_request_ajax_error, get_user_address, get_site_settings
from .payment_verify_views import verify_payment_view
from termos_eshop.Utilities import delete_product_from_cart


def orders_cart_view(req):
    cont = {'site_settings': get_site_settings()}
    # cont = giveme_site_settings_and_category(cont)
    main_order_cart = giveme_cart(req)

    # check that if user has main_Order with Detail_order (cart with products in)
    is_user_has_active_cart_to_show = is_it_filled_cart(req=req, cart=main_order_cart)

    if is_user_has_active_cart_to_show:
        # check it to send main_order_cart or session_cart_items
        if req.user.is_authenticated:
            cont['main_order_cart'] = main_order_cart
            s_settings = cont['site_settings']
            if s_settings.transport_limit:
                if main_order_cart.get_total_price() >= int(s_settings.transport_limit_price):
                    cont['transport_price'] = 0
                else:
                    cont['transport_price'] = int(s_settings.transport_price)
            else:
                cont['transport_price'] = 0
        else:
            # session_cart_items
            cont['session_cart_items'] = main_order_cart
    else:
        #  show the empty Cart
        cont['main_order_cart'] = None

    return render(req, "CartLayout.html", cont)


# --------------------------------------------------- CHECKOUT ---------------------------------------------------
# --------------------------------------------------- CHECKOUT ---------------------------------------------------


@login_required(login_url="/user/login")  # 11/9/2022 m/d/y
def checkout_view(req, **kwargs):

    #  Utilities for process
    cont = {}
    cart_id_for_repay = kwargs.get('repay_cart_id')

    # is user requested to repay an already paid cart ?
    if cart_id_for_repay:
        order_for_repay = Order_Main_Model.objects.filter(id=cart_id_for_repay,
                                                          owner_id=req.user.id,
                                                          is_paid=True,
                                                          payment_status=1)
        if order_for_repay.count() == 1:
            order_for_repay = order_for_repay.first()
        else:
            return redirect("module_orders:urls_cart")
    else:
        order_for_repay = None

    # ////////// ---- ////////// | ////////// ---- //////////

    if req.method == "POST":  # payment_page requested
        if req.POST.get('accept_terms'):  # terms are accepted > goto payment page

            if order_for_repay:
                # goto payment page for unsuccessful paid cart
                return verify_payment_view(request=req, repay_cart_id=order_for_repay.id)
            else:
                # goto payment page for current(unpaid) cart
                return verify_payment_view(req)

        else:
            # show message to accept terms
            cont['force_terms'] = True

    # ////////// ---- ////////// | ////////// ---- //////////

    # show the checkout Page ---------------------------------

    the_address = get_user_address(req)

    # if user address is not completely filled > send user to edit_address page
    if not is_it_perfect_address(the_address):
        return profile_address_edit(req, Referer=reverse("module_orders:urls_checkout"))

    # if user requested to repay an already_paid_cart, then we have to render it else > render current cart
    main_order_cart = giveme_cart(req) if not order_for_repay else order_for_repay

    if main_order_cart.get_amount() == 0:
        # Cart is empty > redirect to cart page
        return redirect("module_orders:urls_cart")

    cont['main_order_cart'] = main_order_cart
    cont['site_settings'] = get_site_settings()

    return render(req, "Checkout.html", cont)


# ---------------------------------------- DELETE Views ----------------------------------------
# ---------------------------------------- DELETE Views ----------------------------------------


# Delete Product from cart page
def ajax_delete_from_cart(req):
    if is_ajax(req):

        # receive request parameters and find the_product
        product_id = req.POST.get('product_id')
        the_product = give_me_the_product_by_id(product_id)
        if the_product is None:
            return bad_request_ajax_error()

        # delete the_product from cart
        delete_product_from_cart(req=req, the_product=the_product)
        main_order_cart = giveme_cart(req)

        # process Start
        if req.user.is_authenticated:
            products_in_cart = Order_Detail_Model.objects.filter(from_Main_order=main_order_cart)

            if products_in_cart.count() == 0:
                # show empty cart
                outer = """
                    <div class="checkout">
                        <div class="form-coupon-toggle">
                            <div class="woocommerce-info">
                                سبد خرید شما خالی است
                            </div>
                        </div>
                    </div>
                """
                response = {'outer': outer, 'amount_of_cart_products': '0'}
            else:
                # show the remained products
                cont = {'site_settings': site_settings.objects.first(), 'main_order_cart': main_order_cart}
                outer = render_to_string(request=req, template_name="includes/CartWithProducts.html", context=cont)
                response = {'outer': outer, 'amount_of_cart_products': main_order_cart.get_amount()}

            return JsonResponse(response, status=200)
        else:
            # User is not logged in >> delete it from sessions
            if main_order_cart.number_of_cart_items:
                # send the response
                cont = {'site_settings': site_settings.objects.first(), 'session_cart_items': main_order_cart}
                outer = render_to_string(request=req, template_name="includes/CartWithProducts.html", context=cont)
                response = {'outer': outer, 'amount_of_cart_products': main_order_cart.number_of_cart_items}
            else:
                outer = """
                    <div class="checkout">
                        <div class="form-coupon-toggle">
                            <div class="woocommerce-info">
                                سبد خرید شما خالی است
                            </div>
                        </div>
                    </div>
                """
                response = {'outer': outer, 'amount_of_cart_products': '0'}

            return JsonResponse(response, status=200)
    return bad_request_ajax_error()


# @csrf_protect
# @login_required(login_url="/user/login")
#  this function is for deleting products from sidebar cart
def ajax_delete_from_sidebar(req):  # 11/04/2022  - m/d/y
    if is_ajax(req):
        # receive request parameters and find the_product
        try:
            product_id = req.POST.get('product_id')
        except KeyError:
            return bad_request_ajax_error()
        the_product = give_me_the_product_by_id(product_id)
        if the_product is None:
            return bad_request_ajax_error()

        # delete the_product from user's cart
        delete_product_from_cart(req, the_product)
        main_order_cart = giveme_cart(req)

        if req.user.is_authenticated:
            outer = partial_sidebar_cart_view(req, render_to_str=True)
            response = {
                'outer': outer,
                'amount_of_cart_products': main_order_cart.get_amount(),
            }
            return JsonResponse(response, status=200)
        else:
            outer = partial_sidebar_cart_view(req, render_to_str=True)
            response = {
                'outer': outer,
                'amount_of_cart_products': main_order_cart.number_of_cart_items,
            }
            return JsonResponse(response, status=200)
    else:
        return bad_request_ajax_error()


# ---------------------------------------- CHANGE COUNT View ----------------------------------------
# ---------------------------------------- CHANGE COUNT View ----------------------------------------

def ajax_change_amount(req):
    if is_ajax(req):
        # receive request parameters and find the_product
        try:
            order_count = req.POST.get('product_count')
            product_id = req.POST.get('product_id')
        except KeyError:
            return bad_request_ajax_error()
        the_product = give_me_the_product_by_id(product_id)
        if the_product is None:
            return bad_request_ajax_error()

        try:
            if int(order_count) <= 0:  # if ther product need to be deleted (requested to amount = 0)
                return ajax_delete_from_cart(req)
        except ValueError:
            return bad_request_ajax_error()

        main_cart = giveme_cart(req)

        if req.user.is_authenticated:
            #  user is logged in - procces on database
            detail_cart, out_of_stock = create_new_or_update_product_in_cart(req=req, order_main=main_cart,
                                                                             order_count=order_count,
                                                                             the_product=the_product, append=False)

            single_price = "{:,}".format(int(the_product.price))
            total_price = detail_cart.total_price_with_comma()
            final_price = 0

            for d_cart in Order_Detail_Model.objects.filter(from_Main_order=main_cart):
                final_price += d_cart.total_price()

            cont = {'site_settings': get_site_settings()}
            sitesettings = cont['site_settings']

            transport_price = int(sitesettings.transport_price)
            if sitesettings.transport_limit:
                if final_price >= int(sitesettings.transport_limit_price):
                    transport_price = 0

            final_price = "{:,}".format(int(final_price))
            transport_price = "{:,}".format(int(transport_price))

            response = {
                'single_price': single_price,
                'total_price': total_price,
                'final_price': final_price,
                'transport_price': transport_price,
                'amount_of_cart_products': main_cart.get_amount(),
                'product_count': main_cart.get_amount_of_product_in_cart(the_product=the_product),
            }

            return JsonResponse(response, status=200)
        else:
            # User is not logged in - procces on sessions
            session_cart_items, out_of_stock = create_new_or_update_product_in_cart(req=req, order_main=None,
                                                                                    order_count=order_count,
                                                                                    the_product=the_product,
                                                                                    append=False)
            single_price = "{:,}".format(int(the_product.price))
            total_price = session_cart_items.get_amount_of_product_in_cart(the_product) * int(the_product.price)
            total_price = "{:,}".format(int(total_price))
            final_price = session_cart_items.total_cart_price_with_comma()
            s_setting = site_settings.objects.all().first()

            transport_price = "{:,}".format(int(s_setting.transport_price))
            if s_setting.transport_limit:
                if session_cart_items.get_total_price() >= int(s_setting.transport_limit_price):
                    transport_price = 0

            response = {
                'single_price': single_price,
                'total_price': total_price,
                'final_price': final_price,
                'transport_price': transport_price,
                'amount_of_cart_products': session_cart_items.number_of_cart_items,
                'product_count': session_cart_items.get_amount_of_product_in_cart(the_product=the_product),
            }

            return JsonResponse(response, status=200)
    else:
        # request is not ajax
        return bad_request_ajax_error()


# --------------------------------------------------- ADD PRODUCT TO CART ---------------------------------------------------
# --------------------------------------------------- ADD PRODUCT TO CART ---------------------------------------------------


def ajax_add_to_cart(req):
    if is_ajax(req):
        try:
            order_count = req.POST.get('product_count')
            product_id = req.POST.get('product_id')
        except KeyError:
            return bad_request_ajax_error()

        the_product = give_me_the_product_by_id(product_id)
        if the_product is None:
            return bad_request_ajax_error()

        # start from here (the req is ajax and the_product found
        main_cart = giveme_cart(req)

        if req.user.is_authenticated:
            # User is logged in then add the Product to DB:
            # add product to user's cart
            detail_cart, out_of_stock = create_new_or_update_product_in_cart(req=req, order_main=main_cart,
                                                                             order_count=int(order_count),
                                                                             the_product=the_product,
                                                                             append=True)

            out_tag = partial_sidebar_cart_view(req, render_to_str=True)
            response = {'out_tag': out_tag, 'out_of_stock': out_of_stock}
            return JsonResponse(response, status=200)

            # -----------------------------
        else:  # User is not Logged in
            # -----------------------------
            # add the_product to seassons because user is not logged in

            session_cart_items, out_of_stock = create_new_or_update_product_in_cart(req=req, order_main=None,
                                                                                    order_count=int(order_count),
                                                                                    append=True,
                                                                                    the_product=the_product)
            # cont = {'session_cart_items': products_in_session(req)}
            # outer_html = render_to_string(request=req, template_name="shared/SidebarCartLayoutForAjax.html",context=cont)
            outer_html = partial_sidebar_cart_view(req, render_to_str=True)

            response = {'out_tag': outer_html, 'out_of_stock': out_of_stock}
            return JsonResponse(response, status=200)
    else:
        return bad_request_ajax_error()


# --------------------------------------------------- Utilities ---------------------------------------------------
# --------------------------------------------------- Utilities ---------------------------------------------------


def is_it_filled_cart(req, cart):
    if req.user.is_authenticated:
        # check_DB_cart
        if cart.get_order_details().count() > 0:
            return True
        else:
            return False
    else:
        # Check_Session Cart
        if cart.number_of_cart_items:
            return True
        else:
            return False


def is_it_perfect_address(the_address: module_users.models.UserAddress):
    all_fields = the_address._meta.get_fields()
    for name in all_fields:
        str_fiend_name = name.attname
        if str_fiend_name != 'id' and str_fiend_name != 'user' and str_fiend_name != 'phone_verify_code' and str_fiend_name != 'phone_verify_date_code':
            field_value = getattr(the_address, str_fiend_name)
            if field_value is None or field_value == '':
                return False
    return True
