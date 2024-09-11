from email.mime.image import MIMEImage
from functools import lru_cache
from .settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from module_SiteSettings.models import site_settings


def email_success_payout(req, main_order_cart, send_to):
    # todo -- send invoice too
    cont = {
        'Main_cart': main_order_cart,
        'site_settings': site_settings.objects.first(),
    }
    html_message = render_to_string(template_name='email_templates/SuccessOrderLayout.html', request=req, context=cont)
    text_message = strip_tags(html_message)
    subject = "ترموس"

    res = EmailMultiAlternatives(
        subject,
        text_message,
        EMAIL_HOST_USER,
        [send_to],
    )
    res.attach_alternative(html_message, "text/html")
    res.attach(logo_data())
    res.send()


@lru_cache()
def logo_data():
    sitesettings = site_settings.objects.first()
    logo_dta = sitesettings.logo.read()
    logo = MIMEImage(logo_dta)
    logo.add_header('Content-ID', '<logo>')
    return logo

# def email_register(req,):
