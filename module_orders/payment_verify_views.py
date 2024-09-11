from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from termos_eshop.Utilities import get_site_settings, get_user_address
from module_orders.models import Order_Main_Model
from module_orders.zarinpal import send_request, verify
from termos_eshop.Utilities import giveme_cart
from termos_eshop.email_sender import email_success_payout
from termos_eshop.smsclass import send_success_sms
from termos_eshop.Utilities import giveme_datetime_now_iran


@login_required(login_url="/user/login")
def verify_payment_view(req, **kwargs):  # 12/09/22  m/d/y

    cont = {'site_settings': get_site_settings()}
    site_settings = cont['site_settings']

    if is_it_come_from_checkout_page(req):
        repay_cart_id = kwargs.get('repay_cart_id')  # repay_cart_id is come from checkout_page

        if repay_cart_id:
            main_order_cart = Order_Main_Model.objects.filter(id=repay_cart_id, owner_id=req.user.id, is_paid=True,
                                                              payment_status=1)

            if main_order_cart.count() == 1:  # Repay requested
                main_order_cart = main_order_cart.first()
            else:
                return redirect("module_orders:urls_checkout")
        else:  # requested to pay current cart
            main_order_cart = giveme_cart(req)  # select current cart

    else:  # check  for zarinpal incomes
        cart_id = kwargs.get('cart_id')
        if req.GET.get('Authority') and req.GET.get('Status') and cart_id:
            main_order_cart = Order_Main_Model.objects.filter(id=cart_id, owner_id=req.user.id)
            if main_order_cart.count() != 1:
                return redirect("module_orders:urls_checkout")
            main_order_cart = main_order_cart.first()
            # we will verify the payment at the lower lines
        else:
            return redirect("module_orders:urls_checkout")

    # transport price process and change it to rials
    total_cart_price = main_order_cart.get_final_price_to_pay() * 10

    if is_it_come_from_checkout_page(req):  # if the request is from checkout page  > goto portal
        # send to portal
        main_order_cart.cart_notes = req.POST.get('order-notes')
        main_order_cart.save()
        try:
            callback = req.build_absolute_uri(reverse("module_orders:urls_verify_payment_callback", kwargs={'cart_id': main_order_cart.id}))
            return send_request(amount_rials=int(total_cart_price), CallbackURL=callback)
        except KeyError:
            return redirect("module_orders:urls_checkout")

    else:  # request is from zarinpal > verify the request

        verify_result = verify(req, amount_rials=total_cart_price)
        address = get_user_address(req)

        # Check the portal answer
        if verify_result['status'] == 100:
            # success
            # check the order_id > Update DB > send user to Success_page
            main_order_cart.is_paid = True
            main_order_cart.payment_date = giveme_datetime_now_iran()
            main_order_cart.payment_status = 0
            # "(۰=موفق ۱=ناموفق ۲=بررسی ۳=لغو شده ۴=مرجوع شده) status"
            main_order_cart.package_status = 0
            # (۰=جمع آوری ۱=پک شده ۲=ارسال‌شده // در حالت مرجوعی : ۰=بررسی ۱=استرداد‌مبلغ ۲=غیر قابل قبول)
            main_order_cart.transaction_id = verify_result['RefID']
            main_order_cart.save()
            put_address_to_card(address=address, paid_cart=main_order_cart, site_settings=site_settings)
            send_success_sms(req.user.get_full_name(), order_id=main_order_cart.get_id_plus_1000(), reciever_num=str(req.user.useradditional.Phone))
            send_success_sms(req.user.get_full_name(), order_id=main_order_cart.get_id_plus_1000(), reciever_num='09187232987')
            email_success_payout(req, main_order_cart, req.user.email)
            return show_success_view(req, order_id=main_order_cart.id)
        elif verify_result['status'] == 101:
            # submitted !
            main_order_cart.is_paid = True
            main_order_cart.payment_date = giveme_datetime_now_iran()
            main_order_cart.payment_status = 2
            # "(۰=موفق ۱=ناموفق ۲=بررسی ۳=لغو شده ۴=مرجوع شده) status"
            main_order_cart.package_status = -1
            main_order_cart.error_message = verify_result['error_message']
            main_order_cart.save()
            put_address_to_card(address=address, paid_cart=main_order_cart, site_settings=site_settings)
            send_success_sms("۱۰۱ ارور", order_id=main_order_cart.id + 1000, reciever_num='09187232987')
            return show_failed_view(req, message=verify_result['error_message'], cart_id=main_order_cart.id)
        elif verify_result['status'] == -1 or verify_result['status'] == 0:
            # failed or has errors
            main_order_cart.is_paid = True
            main_order_cart.payment_date = giveme_datetime_now_iran()
            main_order_cart.payment_status = 1
            # "(۰=موفق ۱=ناموفق ۲=بررسی ۳=لغو شده ۴=مرجوع شده) status"
            main_order_cart.package_status = -1
            main_order_cart.error_message = verify_result['error_message']
            main_order_cart.save()
            put_address_to_card(address=address, paid_cart=main_order_cart, site_settings=site_settings)
            send_success_sms(f"{verify_result['status']} ارور", order_id=main_order_cart.id + 1000, reciever_num='09187232987')
            return show_failed_view(req, message=verify_result['error_message'], cart_id=main_order_cart.id)
        else:
            # payment cancelled by user so keep the cart as active unpaid cart
            return show_failed_view(req=req, message="تراکنش توسط کاربر لغو شد", cart_id=None)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_it_come_from_checkout_page(req):
    try:
        referer = req.headers['Referer']
        order_comment = req.POST.get('order-notes')
        if reverse("module_orders:urls_checkout") in referer and order_comment is not None:
            return True
        else:
            return False
    except KeyError:
        return False


def put_address_to_card(address, paid_cart, site_settings):
    paid_cart.receiver_first_name = address.name
    paid_cart.receiver_last_name = address.family
    paid_cart.receiver_address = address.address_detail
    paid_cart.receiver_phone = address.phone
    paid_cart.receiver_email = address.email
    paid_cart.receiver_postalcode = address.post_code

    if site_settings.transport_limit:  # We have free_shipping option
        if paid_cart.get_total_price() >= site_settings.get_transport_limit_price():
            paid_cart.transport_price = 0
        else:
            paid_cart.transport_price = site_settings.transport_price
    else:
        paid_cart.transport_price = site_settings.transport_price

    paid_cart.save()


def show_success_view(req, order_id):  # 12/09/22  m/d/y
    cont = {'order_id': order_id}
    return render(request=req, template_name="orders_payments/PaymentSuccess.html", context=cont)


def show_failed_view(req, cart_id, message=None):  # 12/09/22  m/d/y
    cont = {
        'message': message,
        'cart_id': cart_id,
    }
    return render(req, template_name="orders_payments/PaymentFailed.html", context=cont)
