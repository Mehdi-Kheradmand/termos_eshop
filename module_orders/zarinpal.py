# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json

MERCHANT = 'e1240a9a-96d7-405b-a23e-e5860eb81b00'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'mehdi.kr@gmail.com'  # Optional
mobile = '09356818853'  # Optional
# Important: need to edit for realy server.
# CallbackURL = 'https://termos.ir/orders/verify/'


def send_request(CallbackURL, amount_rials):
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount_rials,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request, amount_rials: str):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']

    if t_status == 'OK':
        req_header = {
            "accept": "application/json",
            "content-type": "application/json'"
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": str(amount_rials),
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            # No Errors
            t_status = req.json()['data']['code']
            if t_status == 100:
                # success
                response = {'RefID': str(req.json()['data']['ref_id']), 'status': 100}
                return response
            elif t_status == 101:
                # submitted
                response = {'error_message': str(req.json()['data']['message']), 'status': 101}
                return response
            else:
                # failed "-1"
                response = {'error_message': str(req.json()['data']['message']), 'status': -1}
                return response
        else:
            # Has Errors "0"
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return {'error_code': e_code, 'error_message': str(e_message), 'status': 0}
    else:
        # cancelled by user
        return {'error_message': "Transaction failed or canceled by user", 'status': -2}
