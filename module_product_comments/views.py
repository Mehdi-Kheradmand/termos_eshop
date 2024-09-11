from django.contrib.auth.decorators import login_required
from django.conf import settings
from urllib.parse import urlencode
from urllib import request
import json
from django.db.models import Q
from django.http import JsonResponse
from module_product_comments.models import Product_Comments_Model
from module_product_comments.forms import ProductCommentsForm
from termos_eshop.Utilities import is_ajax


# Create your views here.
@login_required(login_url="/user/login")
def ajax_product_comments(req):
    if is_ajax(req):
        username = req.user.username
        comment_form = ProductCommentsForm(req.POST or None)

        if comment_form.is_valid() and req.method == "POST":
            # captcha check
            recaptcha_response = req.POST['g-recaptcha-response']
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urlencode(values).encode()
            _req = request.Request(url, data=data)
            response = request.urlopen(_req)
            result = json.loads(response.read().decode())
            if not result['success']:  # if captcha is successful
                return JsonResponse({'message': 'Unauthorized'}, status=401)

            try:
                comment = req.POST['msg'].strip()
                p_id = req.POST['product_id']
            except KeyError:
                return JsonResponse({'message': 'Bad Request'}, status=400)

            # add new comment
            if comment == '' or comment is None or len(comment) < 10 or len(comment) > 1000:
                return JsonResponse({'is_it_valid': False}, status=200)
            # validated
            add_cm = Product_Comments_Model.objects.create(product_id=p_id, owner_id=req.user.id, msg=comment)
            add_cm.save()

            lookup = (Q(is_accepted=True) | Q(owner__username=username))
            product_comments = Product_Comments_Model.objects.filter(lookup, product_id=p_id).order_by('-created_date')
            ol_tag = ''
            for p_comment in product_comments:
                ol_tag += '<li><div class ="row" ><div class ="col-12 col-sm-9" ><div class ="comment-content" ><div class ="meta" >توسط<strong class ="author" >'
                ol_tag += p_comment.owner.first_name
                ol_tag += '</strong ><span class ="dash" > در تاریخ </ span ><time class ="published-date" >'
                ol_tag += str(p_comment.created_date.day)
                ol_tag += '</time >'
                if not p_comment.is_accepted:
                    ol_tag += '<span class ="alert-warning" > منتظر تایید </span >'
                ol_tag += '</div ><div class ="description" ><p > ' + p_comment.msg + ' </p ></div ></div ></div ></div ></li >'

            return JsonResponse({'is_it_valid': True, 'ol_tag': ol_tag}, status=200)
        else:
            return JsonResponse({'message': 'Bad Request'}, status=400)
    else:
        return JsonResponse({'message': 'Bad Request'}, status=400)
