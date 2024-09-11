from django.http import JsonResponse


def ajax_filter_view(req):
    return JsonResponse('Products to show')
