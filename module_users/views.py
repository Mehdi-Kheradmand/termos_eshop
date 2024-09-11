from django.shortcuts import redirect, render
from django.contrib.auth import logout
from hashlib import sha256
from random import randint
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from module_users.forms import EmailPhoneForm, Form_Password, Form_UserRegister, FormOTP
from module_users.models import UserAddress, UserAdditional
from termos_eshop.Utilities import log_it_in, giveme_a_random_user_num, reset_user_otp, otp_check
from termos_eshop.Utilities import find_user_by_phone, is_ajax, google_recaptcha_verify, is_it_email, \
    find_user_by_email, giveme_datetime_now_iran, giveme_remaining_time_for_verify, is_it_phone_number
from module_SiteSettings.models import site_settings as site_settings_model
from termos_eshop.smsclass import send_otp_sms
# -------------------------------------------- LOGIN ------------------------------------


def login_view(req):
    if req.user.is_authenticated:
        return redirect("module_profile:urls_profile_view")
    site_settings = site_settings_model.objects.first()
    cont = {
        'context_form': EmailPhoneForm,
        'site_settings': site_settings,
        'next_req_addr': reverse("module_users:urls_ajax_email_phone"),
    }
    return render(req, "login/LoginLayout.html", context=cont)


def ajax_email_phone(req):
    received_email_phone_form = EmailPhoneForm(req.POST or None)
    # received_otp_form = Form_OTP(req.POST or None)
    response = {'is_there_error': False, 'status': "Success : 200", 'outer': None, 'reload_recaptcha': False}

    if is_ajax(req):

        if received_email_phone_form.is_valid():
            # User entered phone or Email
            # Captcha test
            recaptcha_response = google_recaptcha_verify(req)
            if not recaptcha_response:  # if captcha is Failed
                response['is_there_error'] = True
                response['reload_recaptcha'] = True
                error_list = ["عبارت امنیتی درست نیست"]
                response['error_list'] = error_list
                return JsonResponse(response, status=200)
            else:  # success captcha
                # check the entered Value
                received_email_phone = received_email_phone_form.cleaned_data.get('input_email_phone')

                if is_it_email(received_email_phone):  # user_entered_Email Address ------------------------------------

                    found_user = find_user_by_email(email=received_email_phone)

                    if found_user:
                        edited_form_password = Form_Password(initial={'input_hidden_email': received_email_phone})
                        cont = {
                            'btn_onclick': "password_exchange(this.id)",
                            'context_form': edited_form_password,
                            'next_req_addr': reverse("module_users:urls_ajax_password"),
                        }
                        outer = render_to_string(request=req, template_name="shared/UserOuterAjaxLayout.html", context=cont)
                        response['outer'] = outer
                        # response['user_phone'] = received_email_phone
                        return JsonResponse(response, status=200)
                    else:
                        # error
                        response['is_there_error'] = True
                        error_list = ["حساب کاربری با این مشخصات پیدا نشد. لطفا برای ثبت نام شماره موبایل خود را وارد "
                                      "کنید"]
                        response['error_list'] = error_list
                        return JsonResponse(response, status=200)

                else:  # Entered Phone Number --------------------------------------------------------------------------
                    # User Entered Phone Number, and it is already checked by forms validators
                    return ajax_otp_reset(req=req, response=response, user_phone_number=received_email_phone)

        else:  # form has Errors ---------------------------------------------------------------------------------------
            error_list = []
            for form_input in received_email_phone_form.errors:
                for error_msg in received_email_phone_form.errors[form_input]:
                    error_list.append(error_msg)
            response['is_there_error'] = True
            response['error_list'] = error_list
            return JsonResponse(response, status=200)
    else:
        return bad_request_ajax_error(response)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def ajax_password(req):
    # the user entered email and password we have to check it
    received_password_form = Form_Password(req.POST or None)
    response = {'is_there_error': False, 'status': "Success : 200", 'outer': None}

    if is_ajax(req=req):
        if received_password_form.is_valid():
            # at the first receive email and password from request
            received_password = received_password_form.cleaned_data.get('input_password')
            received_email = received_password_form.cleaned_data.get('input_hidden_email')
            found_user = find_user_by_email(received_email, received_password)
            if found_user:
                log_it_in(req=req, user=found_user, password=received_password)
                return JsonResponse(response, status=200)  # javascript handle it, and it will redirect to next link

            else:  # user not found
                response['is_there_error'] = True
                error_list = ["گذرواژه درست نیست."]
                response['error_list'] = error_list
                return JsonResponse(response, status=200)

        else:  # form has Errors ---------------------------------------------------------------------------------------
            error_list = []
            for form_input in received_password_form.errors:
                for error_msg in received_password_form.errors[form_input]:
                    error_list.append(error_msg)
            response['is_there_error'] = True
            response['error_list'] = error_list
            return JsonResponse(response, status=200)

    else:
        return bad_request_ajax_error(response)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def ajax_otp(req):  # فرم رمز يكبار مصرف دريافت ميشه كه دو حالت داره - درخواست رمز مجدد - درخواست ورود
    # درخواست ورود دو حالت داره
    # يكي اكانت داراي مشخصات نيست كه بايد فرم دريافت مشخصات بياد ۲- مشخصات داره که یوزر لاگین میشه

    received_form_otp = FormOTP(req.POST or None)
    response = {'is_there_error': False, 'status': "Success : 200", 'outer': None}

    if is_ajax(req=req):
        if received_form_otp.is_valid():
            received_otp = str(received_form_otp.cleaned_data.get('input_otp'))
            received_user_phone = received_form_otp.cleaned_data.get('input_hidden_phone')
            found_user = find_user_by_phone(phone=received_user_phone)
            if found_user:
                # Is user requested to Log-In or resend OTP
                if otp_check(found_user, received_otp):

                    if giveme_remaining_time_for_verify(found_user, 200) >= -5:
                        # OTP code is correct
                        if len(str(found_user.first_name)) < 2:  # Requested to log in - if first_name is emtpy > show register page
                            edited_form_register = Form_UserRegister(initial={
                                'input_hidden_hash_code': found_user.useradditional.phone_verify_hash_code,
                                'input_phone_number': received_user_phone,
                            })
                            cont = {
                                'btn_onclick': "register_func()",
                                'context_form': edited_form_register,
                                'next_req_addr': reverse("module_users:urls_ajax_register"),
                            }
                            outer = render_to_string(request=req, template_name="shared/UserOuterAjaxLayout.html",
                                                     context=cont)
                            response['outer'] = outer
                            # response['user_phone'] = received_user__phone  # what is this
                            return JsonResponse(response, status=200)
                        else:  # user is already created then log in it
                            # login
                            log_it_in(req=req, user=found_user)
                            # goto the next url
                            response['outer'] = None  # it means we have not any html code and js will goto next url
                            return JsonResponse(response, status=200)
                    else:  # Expired VerifyCode Date
                        response['is_there_error'] = True
                        error_list = ["کد تایید منقضی شده. میتوانید از دکمه 'ارسال مجدد' استفاده کنید ."]
                        response['error_list'] = error_list
                        return JsonResponse(response, status=200)
                else:  # Wrong OTP
                    response['is_there_error'] = True
                    error_list = ["کد تایید درست نیست."]
                    response['error_list'] = error_list
                    return JsonResponse(response, status=200)
        else:  # form has Errors ---------------------------------------------------------------------------------------
            error_list = []
            for form_input in received_form_otp.errors:
                for error_msg in received_form_otp.errors[form_input]:
                    error_list.append(error_msg)
            response['is_there_error'] = True
            response['error_list'] = error_list
            return JsonResponse(response, status=200)

    return bad_request_ajax_error(response)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def ajax_otp_reset(req, response=None, user_phone_number=None):
    if is_ajax(req):
        if response is None:
            response = {'is_there_error': False, 'status': "Success : 200", 'outer': None}
        if user_phone_number is None:
            received_form_otp = FormOTP(req.POST or None)
            if received_form_otp.is_valid():
                user_phone_number = received_form_otp.cleaned_data.get('input_hidden_phone')
            else:
                return bad_request_ajax_error(response=response)

        received_email_phone = '0' + str(int(user_phone_number))
        found_user = find_user_by_phone(received_email_phone)
        edited_form_otp = FormOTP(initial={'input_hidden_phone': received_email_phone})
        cont = {
            'btn_onclick': "otp_func(this.id)",
            'context_form': edited_form_otp,
            'next_req_addr': reverse("module_users:urls_ajax_otp"),
        }

        # check request origin
        if not (str(get_current_site(req)) in req.headers['Origin']):
            return bad_request_ajax_error(response)

        if found_user:  # User found

            # create OTP and Timer
            diff_time = giveme_remaining_time_for_verify(user=found_user, timer_value=200)

            if diff_time < 20:  # create new OTP if difference time is under 20 sec
                phone_verify_code = reset_user_otp(found_user)
                response['otp_timer'] = 210
                # send sms
                send_otp_sms(verify_code=phone_verify_code, receiver_num=received_email_phone)
            else:
                # Timer is not expired
                response['otp_timer'] = diff_time

        else:  # new user
            new_random_username = giveme_a_random_user_num()
            new_user_creator: User = User.objects.create_user(
                username=new_random_username,
                password=get_random_string(length=10).lower(),
            )
            new_user_creator.save()

            phone_verify_code = str(randint(100000, 999999))
            phone_verify_hash_code = sha256(phone_verify_code.encode()).hexdigest()
            email_verify_hash_code = sha256(str(User.objects.make_random_password(length=12)).encode()).hexdigest()
            user_additional_creator = UserAdditional.objects.create(
                owner_id=new_user_creator.id,
                Phone=received_email_phone,
                phone_verified=False,
                phone_verify_date_code=giveme_datetime_now_iran(),
                phone_verify_hash_code=phone_verify_hash_code,
                email_verify_hash_code=email_verify_hash_code,
            )
            user_additional_creator.save()

            user_address_creator = UserAddress.objects.create(
                user_id=new_user_creator.id
            )
            user_address_creator.save()
            response['otp_timer'] = 210
            # send sms
            send_otp_sms(verify_code=phone_verify_code, receiver_num=received_email_phone)
        #     ----------------------------------------------------------

        # render outer
        outer = render_to_string(request=req, template_name="shared/UserOuterAjaxLayout.html", context=cont)
        response['outer'] = outer
        return JsonResponse(response, status=200)
    else:
        return bad_request_ajax_error()


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def ajax_register(req):
    received_form_user_register = Form_UserRegister(req.POST or None)

    if is_ajax(req):
        response = {'is_there_error': False, 'status': "Success : 200", 'outer': None}
        if received_form_user_register.is_valid():
            received_hash_code = str(received_form_user_register.cleaned_data.get('input_hidden_hash_code'))
            received_user_phone = received_form_user_register.data.get('input_phone_number')
            received_user_phone = '0' + str(int(received_user_phone))
            if not is_it_phone_number(received_user_phone):
                return bad_request_ajax_error()

            received_first_name = received_form_user_register.cleaned_data.get('input_first_name')
            received_last_name = received_form_user_register.cleaned_data.get('input_last_name')
            received_email = received_form_user_register.cleaned_data.get('input_email')
            received_password = received_form_user_register.cleaned_data.get('input_password')
            found_user = find_user_by_phone(phone=received_user_phone)
            if found_user:
                phone_verify_status = found_user.useradditional.phone_verified
                if otp_check(found_user, received_hash_code, is_code_already_hashed=True):
                    if not phone_verify_status:
                        #  Safe and OK
                        # Register User and Show welcome page
                        found_user.first_name = received_first_name
                        found_user.last_name = received_last_name
                        found_user.email = received_email
                        found_user.useradditional.Phone = received_user_phone
                        found_user.useradditional.phone_verified = True

                        if received_password is not None and received_password != '':
                            found_user.set_password(received_password)

                        found_user.useradditional.save()
                        found_user.save()

                        #  welcome page
                        cont = {
                            'btn_onclick': None,
                            'context_form': None,
                            'next_req_addr': None,
                        }
                        outer = render_to_string(request=req, template_name="shared/UserOuterAjaxLayout.html",
                                                 context=cont)
                        response['outer'] = outer

                        log_it_in(req=req, user=found_user)
                        return JsonResponse(response, status=200)

            return bad_request_ajax_error()
        else:
            error_list = []
            for form_input in received_form_user_register.errors:
                for error_msg in received_form_user_register.errors[form_input]:
                    error_list.append(error_msg)
            response['is_there_error'] = True
            response['error_list'] = error_list
            return JsonResponse(response, status=200)
    else:
        return bad_request_ajax_error()


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def bad_request_ajax_error(response=None):
    if response is None:
        response = {}
    error_list = ["Error 400 -- Bad Request | درخواست نامعتبر"]
    response['is_there_error'] = False
    response['error_list'] = error_list
    return JsonResponse(response, status=400)


def log_out_view(req):
    logout(req)
    return redirect("/")
