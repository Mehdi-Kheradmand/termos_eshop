from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from module_orders.models import Order_Main_Model, Order_Detail_Model
from termos_eshop.Utilities import is_it_numeric, is_it_email, is_it_first_or_last_name, is_it_phone_number, is_ajax, \
    get_user_address, giveme_remaining_time_for_verify, reset_user_otp, otp_check
from module_products.models import Product
from django.shortcuts import render, redirect
from django.urls import reverse
from module_SiteSettings.models import site_settings
from termos_eshop.Utilities import bad_request_ajax_error, log_it_in
from termos_eshop.smsclass import send_otp_sms, send_products_update_sms


@login_required(login_url="/user/login")
def profile_address_edit(req, **kwargs):  # 11/9/2022 m/d/y

    get_user_address(req)  # create new address if not exist

    if req.user.is_authenticated:
        try:
            back_address = kwargs['Referer']
        except KeyError:
            try:
                back_address = req.headers['Referer']
            except KeyError:
                back_address = reverse("module_profile:urls_profile_view")

        cont = {'back_address': back_address, 'site_settings': site_settings.objects.first()}
        return render(req, "profile/AddressEditLayout/AddressEditLayout.html", context=cont)

    else:
        return redirect("module_users:urls_Login_Page")


@login_required(login_url="/user/login")
def profile_address_edit_ajax_view(req):
    if not is_ajax(req):
        return bad_request_ajax_error()
    try:
        first_name = req.POST['name'].strip()
        last_name = req.POST['last_name'].strip()
        state = req.POST['state']
        city = req.POST['city'].strip()
        address = req.POST['address'].strip()
        postcode = req.POST['postcode']
        phone = req.POST['phone'].strip()
        email = req.POST['email'].strip()
        # back_link = req.POST['back_address']
    except KeyError:
        return bad_request_ajax_error()
    error_list = check_address_form(first_name, last_name, state, city, address, postcode, phone, email)

    if not error_list['is_there_error']:
        # save address
        db_address = get_user_address(req)
        db_address.name = first_name
        db_address.family = last_name
        db_address.state = state
        db_address.city = city
        db_address.address_detail = address
        db_address.post_code = postcode
        db_address.phone = phone
        db_address.email = email
        db_address.save()
        # The process is Done

    response = {'error_list': error_list}
    return JsonResponse(response, status=200)


def check_address_form(first_name, last_name, state, city, address, postcode, phone, email):
    error_list = {
        'first_name': False, 'last_name': False, 'state': False,
        'city': False, 'address': False, 'postcode': False, 'phone': False, 'email': False, 'is_there_error': False
    }
    state = int(state)

    if (not is_it_first_or_last_name(first_name)) or first_name == '' or len(first_name) > 250 or len(first_name) < 3:
        error_list['first_name'] = True
        error_list['is_there_error'] = True

    if (not is_it_first_or_last_name(last_name)) or last_name == '' or len(last_name) > 250 or len(last_name) < 3:
        error_list['last_name'] = True
        error_list['is_there_error'] = True

    if (not is_it_numeric(state)) or state == 0 or state > 32:
        error_list['state'] = True
        error_list['is_there_error'] = True

    if (not is_it_first_or_last_name(city)) or city == '' or len(city) > 50 or len(city) < 2:
        error_list['city'] = True
        error_list['is_there_error'] = True

    if address is None or address == '' or len(address) > 250 or len(address) < 8:
        error_list['address'] = True
        error_list['is_there_error'] = True

    if (not is_it_numeric(postcode)) or len(postcode) != 10:
        error_list['postcode'] = True
        error_list['is_there_error'] = True

    if not is_it_email(email):
        error_list['email'] = True
        error_list['is_there_error'] = True

    if not is_it_phone_number(phone):
        error_list['phone'] = True
        error_list['is_there_error'] = True

    return error_list


# --------------------------------------------------------------- Profile View ----------------------------------------
# --------------------------------------------------------------- Profile View ----------------------------------------

@login_required(login_url="/user/login")
def profile_view(req):
    if User.is_authenticated and req.user.id is not None:
        # user is logged in
        user_id = req.user.id
        cont = {}
        wish_list = Product.objects.filter(wisher_users=req.user)
        cont['wish_list'] = wish_list
        cont['user_paid_orders'] = Order_Main_Model.objects.filter(owner_id=user_id, is_paid=True)
        cont['site_settings'] = site_settings.objects.first()
        return render(req, "profile/ProfileLayout/ProfileLayout.html", cont)
    else:
        return redirect("module_users:urls_Login_Page")


# --------------------------------------------------------------- OrdersList(order history) View ----------------------
# --------------------------------------------------------------- OrdersList(order history) View ----------------------
@login_required(login_url="/user/login")
def orders_list_view(req):
    # we need all main maincarts(header_cart)
    if User.is_authenticated and req.user.id is not None:
        # user is logged in
        user_id = req.user.id
        main_cart = Order_Main_Model.objects.filter(owner_id=user_id, is_paid=True)
        cont = {
            'header_cart': main_cart,
            'site_settings': site_settings.objects.first(),
        }
        return render(req, "profile/OrdersLayouts/OrdersLayout.html", cont)
    else:
        return redirect("module_users:urls_Login_Page")


# --------------------------------------------------------------- Order Detail ----------------------------------------
# --------------------------------------------------------------- Order Detail ----------------------------------------


@login_required(login_url="/user/login")
def order_detail(req, order_id):
    main_order = Order_Main_Model.objects.filter(id=order_id, owner_id=req.user.id, is_paid=True)
    if main_order.count() != 1:
        raise Http404("صفحه مورد نظر یافت نشد 1010")
    main_order = main_order.first()
    detail_orders = Order_Detail_Model.objects.filter(from_Main_order=main_order)
    cont = {'detail_orders': detail_orders, 'main_order': main_order, 'site_settings': site_settings.objects.first()}

    return render(req, "profile/OrdersLayouts/OrderDetailLayout.html", cont)


# --------------------------------------------------------------- Wishlist View ---------------------------------------
# --------------------------------------------------------------- Wishlist View ---------------------------------------


@login_required(login_url="/user/login")
def wishlist_view(req):
    cont = {'wish_list': Product.objects.filter(wisher_users=req.user)}

    return render(req, "profile/Wishlist/Wishlist.html", cont)


# --------------------------------------------------------------- Edit Profile View -----------------------------------
# --------------------------------------------------------------- Edit_profile View -----------------------------------


@login_required(login_url="/user/login")
def edit_profile_view(req):  # 12/05/22  m/d/y
    if is_ajax(req):
        try:
            first_name = req.POST['first_name'].strip()
            last_name = req.POST['last_name'].strip()
            email = req.POST['email'].strip()
            phone = req.POST['phone'].strip()
            new_password = req.POST['new_pass'].strip()
            verify_code = req.POST['verify_code'].strip()
            in_verify_form = req.POST['in_verify_form']
        except KeyError:
            return bad_request_ajax_error()

        # Options
        error_list = {
            'first_name': False, 'last_name': False,
            'email': False, 'phone': False,
            'new_pass': False, 'verify_code': False,
            'wait_message': False
        }
        has_it_error = False

        # check Inputs
        if not is_it_first_or_last_name(first_name):
            error_list['first_name'] = True
            has_it_error = True
        if not is_it_first_or_last_name(last_name):
            error_list['last_name'] = True
            has_it_error = True

        if not is_it_email(email):
            error_list['email'] = True
            has_it_error = True
        elif User.objects.filter(email__exact=email).count():
            for found_user in User.objects.filter(email__exact=email).all():
                if found_user != req.user:
                    error_list['email'] = True
                    has_it_error = True

        if not is_it_phone_number(phone):
            error_list['phone'] = True
            has_it_error = True
        elif User.objects.filter(useradditional__Phone=phone).count():
            for found_user in User.objects.filter(useradditional__Phone=phone).all():
                if found_user != req.user:
                    error_list['phone'] = True
                    has_it_error = True

        if new_password is not None and new_password != '':
            if len(new_password) < 8 or len(new_password) > 50:
                error_list['new_pass'] = True
                has_it_error = True
        if is_it_numeric(verify_code) and len(verify_code) != 6:  # Code check lvl-1 (not empty and be 6 digits)
            error_list['verify_code'] = True
            has_it_error = True

        #  ---------------------------------------------------

        if not has_it_error:  # There is no error

            # check OTP timer

            # checking that is information changed ?!! or not
            info_changed = True
            if first_name == req.user.first_name and \
                    last_name == req.user.last_name and \
                    email == req.user.email and \
                    phone == req.user.useradditional.Phone:
                if new_password is not None and new_password != '':
                    if req.user.check_password(new_password):
                        info_changed = False
                else:
                    info_changed = False

            if info_changed:  # User information want to be changed
                # is it from verify_form or regular_form
                if in_verify_form:
                    # check verify_Code level 2
                    if otp_check(the_user=req.user, received_otp_code=verify_code):
                        #  Update
                        user_update = User.objects.filter(username=req.user.username).first()
                        if new_password is not None and new_password != '':
                            user_update.set_password(new_password)
                        if email is not None and email != '' and email != req.user.email:
                            user_update.email = email
                        if first_name is not None and first_name != '' and first_name != req.user.first_name:
                            user_update.first_name = first_name
                        if last_name is not None and last_name != '' and last_name != req.user.last_name:
                            user_update.last_name = last_name

                        if phone != req.user.useradditional.Phone and \
                                phone == user_update.useradditional.new_phone_to_change:
                            user_update.useradditional.Phone = user_update.useradditional.new_phone_to_change
                            user_update.useradditional.phone_verified = True
                            user_update.useradditional.save()

                        user_update.save()
                        log_it_in(req, user_update)
                    else:  # wrong OTP
                        error_list['verify_code'] = True
                        has_it_error = True
                else:  # send(reset) OTP > show verify button

                    remaining_time = giveme_remaining_time_for_verify(req.user, 180)

                    if remaining_time < 10:
                        req.user.useradditional.new_phone_to_change = phone
                        req.user.useradditional.save()
                        remaining_time = 180
                        send_otp_sms(reset_user_otp(the_user=req.user), phone)
                    else:
                        if req.user.useradditional.new_phone_to_change != phone:  # phone is new then user have to w8
                            error_list['wait_message'] = True
                            response = {'error_list': error_list, 'success_msg': False}
                            return JsonResponse(response, status=200)

                    # return > returning with no error and no success_msg means to show verify button (for front)
                    response = {'error_list': error_list, 'success_msg': False, 'my_timer': remaining_time}
                    return JsonResponse(response, status=200)

        # Return
        response = {'error_list': error_list, 'success_msg': (not has_it_error)}
        return JsonResponse(response, status=200)

    else:  # Not ajax Request
        cont = {'remaining_time': giveme_remaining_time_for_verify(req.user)}
        return render(req, "profile/EditProfile/EditProfileLayout.html", cont)

#  ------------------------------------------------------------------------------------------
#  ------------------------------------------------ SELLER -----------------------------
#  ------------------------------------------------------------------------------------------


@login_required(login_url="/user/login")
def seller_main_view(req):
    error_list = {'stock_price': False, 'title': False}
    data = {}

    if not is_ajax(req):
        cont = {}
        if req.user.useradditional.IsSeller:
            if req.user.is_superuser:
                cont['allActiveProducts'] = Product.objects.get_active_products().order_by('Seller')
                tst = Product.objects.get_active_products().first()
            return render(request=req, template_name="profile/Seller/SellerMain_Layout.html", context=cont)
        else:
            return redirect(to="module_profile:urls_profile_view")
    else:
        thePost = dict(req.POST)
        index = 0
        error = False

        # Verify Values
        for productId in thePost['DataId[]']:
            if not is_it_numeric(productId):
                return bad_request_ajax_error()

        for pTitle in thePost['DataTitle[]']:
            if pTitle == '' or pTitle is None:
                error_list['title'] = True
                error = True

        for pstock in thePost['DataStock[]']:
            if pstock == '' or pstock is None:
                error_list['stock_price'] = True
                error = True

        for psPrice in thePost['DataPrice[]']:
            if psPrice == '' or psPrice is None:
                error_list['stock_price'] = True
                error = True

        # Save Values
        if not error:
            changedIds = ''

            for productId in thePost['DataId[]']:

                if not req.user.is_superuser:
                    the_product = Product.objects.filter(id=productId, Seller=req.user, active=True)
                else:  # superUser (Show all Products)
                    the_product = Product.objects.filter(id=productId, active=True)

                if the_product.count() == 1:
                    the_product = the_product.first()

                    sendSmsNeeded = False
                    saveNeeded = False

                    if the_product.title != thePost['DataTitle[]'][index].strip():
                        the_product.title = thePost['DataTitle[]'][index].strip()
                        saveNeeded = True

                    if the_product.stock != int(thePost['DataStock[]'][index].strip().replace(',', '')):
                        the_product.stock = int(thePost['DataStock[]'][index].strip().replace(',', ''))
                        saveNeeded = True
                        sendSmsNeeded = True

                    if the_product.IncomingPrice != int(thePost['DataPrice[]'][index].strip().replace(',', '')):
                        the_product.IncomingPrice = int(thePost['DataPrice[]'][index].strip().replace(',', ''))
                        saveNeeded = True
                        sendSmsNeeded = True

                    #  Only For SuperUsers
                    if req.user.is_superuser:
                        sendSmsNeeded = False
                        if the_product.price != int(thePost['DataSellPrice[]'][index].strip().replace(',', '')):
                            the_product.price = int(thePost['DataSellPrice[]'][index].strip().replace(',', ''))
                            saveNeeded = True

                    if saveNeeded:
                        the_product.save()

                    if sendSmsNeeded:
                        if changedIds == '':
                            changedIds = str(productId)
                        else:
                            changedIds += ',' + str(productId)
                else:
                    return bad_request_ajax_error()
                index += 1

            if changedIds != '':  # we have updates product(s)
                # Send SMS
                ids_pack = ''
                if len(changedIds.split(',')) > 10:  # slice sms to 10 ids
                    for _id in changedIds.split(','):
                        if ids_pack == '':
                            ids_pack = str(_id)
                        else:
                            ids_pack += ',' + str(_id)
                        if len(ids_pack.split(',')) % 10 == 0:
                            send_products_update_sms(product_ids=changedIds, receiver_num="09187232987")
                            send_products_update_sms(product_ids=changedIds, receiver_num="09014993447")
                            ids_pack = ''
                    if ids_pack != '':
                        send_products_update_sms(product_ids=changedIds, receiver_num="09187232987")
                        send_products_update_sms(product_ids=changedIds, receiver_num="09014993447")
                else:
                    send_products_update_sms(product_ids=changedIds, receiver_num="09187232987")
                    send_products_update_sms(product_ids=changedIds, receiver_num="09014993447")

        # return
        data['error_list'] = error_list
        return JsonResponse(data, status=200)
