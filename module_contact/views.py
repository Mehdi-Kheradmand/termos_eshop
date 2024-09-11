from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlencode
from urllib import request
import json
# Create your views here.
from termos_eshop.Utilities import is_ajax, is_it_email
from termos_eshop.Utilities import giveme_cart, get_site_settings
from .forms import contact_us_form
from .models import ContactUsForm_Model


def contact_view(req):  # 12/11/22 m/d/y
    cont = {
        'GOOGLE_SITE_KEY': settings.GOOGLE_SITE_KEY,
        'site_settings': get_site_settings(),
        'contact_us_form': contact_us_form,
    }

    if is_ajax(req):
        try:
            name: str = req.POST['form_name'].strip()
            email: str = req.POST['form_email']
            title: str = req.POST['form_title'].strip()
            message: str = req.POST['form_message'].strip()
            recaptcha_response = req.POST['g-recaptcha-response']
        except KeyError:
            return JsonResponse('Bad Request', status=400)

        # Validate
        is_it_valid = True
        error_list = {'name': False,
                      'title': False,
                      'email': False,
                      'message': False,
                      'captcha': False,
                      }

        # captcha Validate
        # url = 'https://www.google.com/recaptcha/api/siteverify'
        url = 'https://www.recaptcha.net/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urlencode(values).encode()
        _req = request.Request(url, data=data)
        response = request.urlopen(_req)
        result = json.loads(response.read().decode())
        if not result['success']:  # if captcha is  not successful
            is_it_valid = False
            error_list['captcha'] = True

        if len(name) < 3 or len(name) > 50:
            error_list['name'] = True
            is_it_valid = False
        if len(title) < 2 or len(title) > 120:
            error_list['title'] = True
            is_it_valid = False
        if len(message) < 3 or len(message) > 1000:
            error_list['message'] = True
            is_it_valid = False
        if not is_it_email(email):
            error_list['email'] = True
            is_it_valid = False

        response = {'error_list': error_list, 'is_it_valid': is_it_valid}

        if not is_it_valid:
            return JsonResponse(response, status=200)
        else:
            # Validated and now we have to save the message
            query = ContactUsForm_Model.objects.create(name=name, email=email, title=title, msg=message)
            query.save()
            return JsonResponse(response, status=200)

    else:
        return render(req, "contact/ContactLayout.html", cont)
