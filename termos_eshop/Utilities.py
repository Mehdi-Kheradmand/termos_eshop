import re
from datetime import datetime
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from hashlib import sha256
from django.shortcuts import redirect
from module_SiteSettings.models import site_settings
from module_orders.models import Order_Detail_Model, Order_Main_Model
# from module_products.models import Product
from urllib.parse import urlencode
from urllib import request as lib_request
import json
from django.contrib.auth import login, authenticate
from random import randint

from module_products.models import Product
from module_users.models import UserAdditional, UserAddress

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'09(\d{9})$'
# fname_lname_regex = r"/^[آ-ی ,.'-, آ-ی]+$/i"
fname_lname_regex1 = r"^[آ-ی]*"
fname_lname_regex2 = r"[آ-ی]$*"


def is_it_email(_email):
    if re.fullmatch(email_regex, _email):
        return True
    else:
        return False


def is_it_numeric(txt):
    if txt is None or txt == '':
        return False
    if type(txt) is int:
        return True
    for char in txt:
        if not char.isdigit():
            return False
    return True


def is_it_password_with_nums_and_letters(password: str, min_len=8, max_len=50):
    if password is None:
        return False

    if (len(password) < min_len) or (len(password) > max_len):
        return False

    have_letter = False
    have_num = False

    for char in password:
        if char.isdigit():
            have_num = True
        elif char.isalpha():
            have_letter = True

    return have_letter and have_num


def is_it_phone_number(phone):
    if phone is None or phone == '':
        return False
    if is_it_numeric(phone):
        int_phone = int(phone)
    else:
        return False
    if (phone[0] != '0' or phone[1] != '9') and (phone[0] != '۰' or phone[1] != '۹'):
        return False
    if re.fullmatch(phone_regex, '0' + str(int_phone)):
        return True
    else:
        return False


def giveme_datetime_now_iran():
    return datetime.now(tz=pytz.timezone('Iran'))


def find_user_by_email(email: str, password: str = None):
    user = User.objects.filter(email=email)
    if user.count() == 1:
        user = user.first()
        if password:
            if user.check_password(password):
                return user
            else:
                return None
        return user
    return None


def find_user_by_phone(phone, password: str = None):
    user = User.objects.filter(useradditional__Phone=phone)
    if user.count() != 1:
        return None
    else:
        user = user.first()
        if password is not None:
            if user.check_password(password):
                return user
            else:
                return None
        else:
            return user


def is_it_first_or_last_name(name: str):
    if name is None or name == '':
        return False
    name = name.replace(' ', '')
    if re.fullmatch(fname_lname_regex1, name) and re.fullmatch(fname_lname_regex1, name):
        if len(name) > 2:
            return True
    return False


def is_ajax(req):
    if req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return True
    return False


def google_recaptcha_verify(req):
    recaptcha_response = req.POST.get('g_recaptcha_response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urlencode(values).encode()
    recaptcha_req = lib_request.Request(url, data=data)
    recaptcha_response = lib_request.urlopen(recaptcha_req)
    recaptcha_result = json.loads(recaptcha_response.read().decode())

    if recaptcha_result['success']:
        return True
    return False


def giveme_remaining_time_for_verify(user: User, timer_value: int = 200):
    now_date = giveme_datetime_now_iran()
    try:
        user_phone_verify_date = user.useradditional.phone_verify_date_code
        if user_phone_verify_date:
            user_phone_verify_date = user_phone_verify_date.astimezone(pytz.timezone('Iran'))
            time_diff = (now_date - user_phone_verify_date).seconds
            time_diff = timer_value - time_diff
            return time_diff if time_diff > 0 else 0
    except ObjectDoesNotExist:
        user_additional_creator = UserAdditional.objects.create(owner_id=user.id)
        user_additional_creator.save()
    return 0


def log_it_in(req, user: User, password=None):
    if user is not None:

        if password:
            rdy_to_login = authenticate(username=user.username, password=password)
        else:
            rdy_to_login = user

        # keep Session for after login
        sessions = EshopSessions(req)
        login(request=req, user=rdy_to_login)
        append_session_to_db(req=req, eshop_sessions=sessions)
        return user

    return None


def giveme_a_random_user_num():
    num = randint(10000, 99999)
    while True:
        if User.objects.filter(username=num).count() > 0:
            num = randint(10000, 99999)
        else:
            return num


def bad_request_ajax_error(response=None):
    if response is None:
        response = {}
    error_list = ["Error 400 -- Bad Request | درخواست نامعتبر"]
    response['is_there_error'] = False
    response['error_list'] = error_list
    return JsonResponse(response, status=400)


def get_user_address(req):
    address = req.user.useraddress_set.all()

    if address.count() == 0:
        address = UserAddress.objects.create(
            user=req.user,
            phone=req.user.useradditional.Phone,
            name=req.user.first_name,
            family=req.user.last_name,
            email=req.user.email)
        address.save()
    else:
        address = address.first()

    return address


def get_site_settings():

    finder = site_settings.objects.filter(active=True)

    if finder.count() == 0:
        finder = site_settings.objects.all()
        if finder.count() == 0:
            new_setting = site_settings.objects.create(active=True)
            new_setting.save()
            return new_setting

    s_settings = finder.first()
    return s_settings


def reset_user_otp(the_user: User):
    now_date = giveme_datetime_now_iran()
    phone_verify_code = str(randint(100000, 999999))
    phone_verify_hash_code = sha256(phone_verify_code.encode()).hexdigest()

    the_user.useradditional.phone_verify_hash_code = phone_verify_hash_code
    the_user.useradditional.phone_verify_date_code = now_date
    the_user.useradditional.save()
    return phone_verify_code


def otp_check(the_user, received_otp_code, is_code_already_hashed=False):

    if received_otp_code is None or received_otp_code == '':
        return False

    if not is_code_already_hashed:  # not Hashed then check numeric
        received_otp_code = str(int(received_otp_code))  # change farsi numbers to eng
        if not is_it_numeric(received_otp_code):
            return False
    else:  # Hashed then check length
        if len(received_otp_code) != 64:
            return False

    db_phone_verify_hash = the_user.useradditional.phone_verify_hash_code

    if is_code_already_hashed:
        received_otp_hash = received_otp_code
    else:
        received_otp_hash = sha256(received_otp_code.encode()).hexdigest()

    if db_phone_verify_hash == received_otp_hash:
        return True
    return False


#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def give_me_the_product_by_id(p_id):
    if not is_it_numeric(p_id):
        return None
    the_product = Product.objects.filter(id=p_id, active=True)
    if the_product.count() != 0:
        return the_product.first()
    return None


# todo --  is this function used anywhere
def add_new_product(req):
    product_id = None
    order_count = None
    if len(req.POST) != 0:
        try:
            product_id = req.POST['product_id']
            order_count = req.POST['order_count']
        except TypeError:
            raise "صفحه مورد نظر یافت نشد (۱۰۰۱)"

    the_product = give_me_the_product_by_id(product_id)
    if the_product is None:
        raise "صفحه مورد نظر یافت نشد -- ۱۰۰۲"

    # now let's add product to database or sessions >>

    if req.user.is_authenticated:
        # user is logged in (add the product in the database) let's find main_cart: Order_main
        main_cart = giveme_cart(req.user.id)
        create_new_or_update_product_in_cart(req, main_cart, order_count, the_product)
    else:
        # user is not logged in (Put the request to the sessions)
        create_new_or_update_product_in_cart(req, order_main=None, order_count=order_count, the_product=the_product)

    # if user refresh the page - form will not be sent again
    return redirect("module_orders:urls_cart")


#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# this function will update user cart prices and returns the order_main(Order_main) or session_cart
def giveme_cart(req):
    if req.user.is_authenticated:
        # user is logged in
        main_cart = Order_Main_Model.objects.filter(is_paid=False, owner_id=req.user.id)

        if main_cart.count() == 0:
            main_cart = Order_Main_Model.objects.create(owner=req.user, is_paid=False)
            main_cart.save()
            return main_cart
        else:
            main_cart = main_cart.first()
            main_cart.update_prices()
            return main_cart
    else:
        return EshopSessions(req)


#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# todo -- Check it carefully many times
def create_new_or_update_product_in_cart(req, order_main, order_count: int, the_product: Product, append=True):
    # return Options
    out_of_stock = False
    order_detail = None

    if the_product.stock < 1:
        out_of_stock = True
        return order_detail, out_of_stock

    if req.user.is_authenticated:
        # is it already created?
        order_detail = Order_Detail_Model.objects.filter(from_Main_order_id=order_main.id, product=the_product)

        if order_detail.all().count() != 0:
            order_detail = order_detail.first()
            # Update Price
            order_detail.price = the_product.price
            # append or Not
            if append:
                # check the stock of product
                if the_product.stock > (order_detail.count + int(order_count)):
                    order_detail.count += int(order_count)
                else:
                    order_detail.count = the_product.stock
                    out_of_stock = True
            else:
                # check the stock of product
                if the_product.stock > int(order_count):
                    order_detail.count = order_count
                else:
                    order_detail.count = the_product.stock
                    out_of_stock = True
            # save and return
            order_detail.save()
            return order_detail, out_of_stock
        else:
            # create new Detail_cart

            if the_product.stock > int(order_count):
                order_detail = Order_Detail_Model.objects.create(
                    from_Main_order_id=order_main.id, count=order_count, price=the_product.price, product=the_product
                )
            else:
                order_detail = Order_Detail_Model.objects.create(
                    from_Main_order_id=order_main.id, count=the_product.stock, price=the_product.price,
                    product=the_product
                )
                out_of_stock = True
            # save and return
            order_detail.save()
            return order_detail, out_of_stock

    else:  # --------   Add to Sessions ---------------------------------------------- /\/\/\/\/\/\/\/\//\/\/\/\/\
        # User is Not logged in :
        session_cart_items = EshopSessions(req)
        # product_id_in_string = str(the_product.id)
        out_of_stock = session_cart_items.update_or_add_product(the_product=the_product, qty=int(order_count),
                                                                append=append)
        # save and return
        session_cart_items.save(req)
        return session_cart_items, out_of_stock


#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#         ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


def delete_product_from_cart(req, the_product):
    if req.user.is_authenticated:
        # delete from database
        detail_cart_for_delete = Order_Detail_Model.objects.filter(product=the_product,
                                                                   from_Main_order__owner_id=req.user.id,
                                                                   from_Main_order__is_paid=False)
        if detail_cart_for_delete.count() == 1:
            detail_cart_for_delete = detail_cart_for_delete.first()
            detail_cart_for_delete.delete()
            # detail_cart_for_delete.save()
    else:
        # delete from sessions
        session_cart_items = EshopSessions(req)
        session_cart_items.delete(the_product=the_product)
        session_cart_items.save(req)


#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#         +++++++++++++++++++++++++++++++++++++++ Session Utilities
#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


class EshopSessions:

    def __init__(self, req):
        self.__number_of_cart_items = 0
        self.__products_list = []
        self.__products_count_list = []
        self.__products_total_prices_list = []
        self.__wish_list = []
        cart_items = req.session.get('cart_items')
        wishlist_items = req.session.get('wishlist_items')

        if cart_items:
            for p_id in cart_items:
                the_product = give_me_the_product_by_id(p_id)
                if the_product:
                    self.__products_list.append(the_product)
                    self.__products_count_list.append(cart_items[p_id])
                    self.__products_total_prices_list.append("{:,}".format(int(the_product.price) * int(cart_items[p_id])))
                    self.__number_of_cart_items += int(cart_items[p_id])

        if wishlist_items:
            for p_id in wishlist_items:
                the_product = give_me_the_product_by_id(p_id)
                if the_product:
                    self.__wish_list.append(the_product)

    #             --------------------------------------------------

    @property
    def number_of_cart_items(self):
        return self.__number_of_cart_items

    @property
    def products_list(self):
        return self.__products_list

    @property
    def products_count_list(self):
        return self.__products_count_list

    @property
    def products_total_prices_list(self):
        return self.__products_total_prices_list

    @property
    def wish_list(self):
        return self.__wish_list

    @number_of_cart_items.setter
    def number_of_cart_items(self, val):
        self.__number_of_cart_items = val

    @products_list.setter
    def products_list(self, val):
        self.__products_list = val

    @products_count_list.setter
    def products_count_list(self, val):
        self.__products_count_list = val

    @products_total_prices_list.setter
    def products_total_prices_list(self, val):
        self.__products_total_prices_list = val

    @wish_list.setter
    def wish_list(self, val):
        self.__wish_list = val

    def total_cart_price_with_comma(self):
        total_price = 0
        id_in_list = 0
        for product in self.products_list:
            total_price += product.price * self.products_count_list[id_in_list]
            id_in_list += 1
        return "{:,}".format(int(total_price))

    def get_total_price(self):
        total_price = 0
        id_in_list = 0
        for product in self.products_list:
            total_price += product.price * self.products_count_list[id_in_list]
            id_in_list += 1
        return int(total_price)

    def get_amount_of_product_in_cart(self, the_product):
        id_in_list = 0
        for product in self.products_list:
            if product == the_product:
                return self.products_count_list[id_in_list]
            id_in_list += 1
        return 0

    def update_or_add_product(self, the_product: Product, qty: int, append=True):
        out_of_stock = False
        id_in_list = 0
        add_new = True

        #  delete
        if qty <= 0 and not append:
            return self.delete(the_product)

        for product in self.products_list:
            if product == the_product:
                add_new = False
                if append:
                    if the_product.stock > (self.products_count_list[id_in_list] + qty):
                        self.products_count_list[id_in_list] += qty
                        self.products_total_prices_list[id_in_list] = str(qty * int(the_product.price))
                        self.number_of_cart_items += qty
                    else:
                        self.number_of_cart_items += the_product.stock
                        self.number_of_cart_items -= self.products_count_list[id_in_list]
                        self.products_count_list[id_in_list] = the_product.stock
                        self.products_total_prices_list[id_in_list] = str(int(the_product.stock) * int(the_product.price))
                        out_of_stock = True
                else:
                    if the_product.stock > qty:
                        self.number_of_cart_items -= self.products_count_list[id_in_list]
                        self.products_count_list[id_in_list] = qty
                        self.number_of_cart_items += qty
                        self.products_total_prices_list[id_in_list] = str(qty * int(the_product.price))
                    else:
                        self.number_of_cart_items -= self.products_count_list[id_in_list]
                        self.products_count_list[id_in_list] = the_product.stock
                        self.number_of_cart_items += the_product.stock
                        self.products_total_prices_list[id_in_list] = str(int(the_product.stock) * int(the_product.price))
                        out_of_stock = True
            id_in_list += 1
        if add_new:
            self.products_list.append(the_product)
            if the_product.stock > qty:
                self.products_count_list.append(qty)
                self.number_of_cart_items += qty
                self.products_total_prices_list.append(str(qty * int(the_product.price)))
            else:
                self.products_count_list.append(the_product.stock)
                self.number_of_cart_items += the_product.stock
                self.products_total_prices_list.append(str(int(the_product.stock) * int(the_product.price)))
                out_of_stock = True
        return out_of_stock

    def delete(self, the_product):
        id_in_list = 0
        for product in self.products_list:
            if product == the_product:
                self.products_list.pop(id_in_list)
                num = self.products_count_list.pop(id_in_list)
                self.number_of_cart_items -= num
                self.products_total_prices_list.pop(id_in_list)
            id_in_list += 1
        if the_product.stock > 0:  # return out-of-stock status
            return False
        return True

    def save(self, req):
        p_dic = {}
        # w_list = []
        index = 0
        for product in self.__products_list:
            p_dic[product.id] = self.products_count_list[index]
            index += 1
        # for product in self.__wish_list:
        #     w_list.append(product.id)
        req.session['cart_items'] = p_dic
        # req.session['wishlist_items'] = w_list

    def get_final_price_to_pay_with_comma(self):
        total_price = self.get_total_price()
        s_settings = site_settings.objects.all().first()
        if s_settings.transport_limit:
            if int(total_price) >= int(s_settings.transport_limit_price):
                return "{:,}".format(total_price)
        return "{:,}".format(total_price + int(s_settings.transport_price))

    def update_wishlist(self, the_product):
        for pr in self.__wish_list:
            if pr == the_product:
                self.__wish_list.remove(the_product)
                return False
        self.__wish_list.append(the_product)
        return True

    def is_product_in_wishlist(self, the_product):
        for pr in self.__wish_list:
            if pr == the_product:
                return True
        return False

#     --------------------------------------------------------------------------------------------------


def append_session_to_db(req, eshop_sessions: EshopSessions):
    if req.user.is_authenticated:
        if eshop_sessions.number_of_cart_items:
            main_cart = giveme_cart(req)
            for_iterate = 0

            for ses_product in eshop_sessions.products_list:
                create_new_or_update_product_in_cart(
                        the_product=ses_product,
                        req=req,
                        order_main=main_cart,
                        order_count=eshop_sessions.products_count_list[for_iterate],
                    )

                for_iterate += 1

#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#         <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
