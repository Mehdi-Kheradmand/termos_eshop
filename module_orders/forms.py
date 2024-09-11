from django import forms
from django.http import Http404
from module_products.models import Product
from module_orders.models import Order_Detail_Model

# خیلیم راحته


class add_order_form(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput())
    order_count = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'step': '1', 'value': '1'}))

    # def give_me_count(self):
    #     return self.fields['order_count']

    class Meta:
        model = Product
        fields = 'stock'

    # __init__ will be run when make new object as this class
    def __init__(self, *args, **kwargs):
        if len(kwargs.items()) != 0:
            kw = kwargs['initial']
            the_product = kw['the_product']
            # the_user = kw['the_user']
            in_cart_qty = kw['found_product_count']
            if the_product:
                # the_product = Product.objects.filter(id=pid)
                # if the_product.count() != 1:
                #     raise Http404("صفحه مورد نظر یافت نشد")
                # the_product = the_product.first()
                start_val = the_product.stock - in_cart_qty
                min_val = 1
                if start_val > 0:
                    start_val = 1
                else:
                    start_val = 0
                    min_val = 0
                super(add_order_form, self).__init__(*args, **kwargs)
                self.fields['order_count'].widget.attrs.update({'max': (the_product.stock-in_cart_qty), 'value': start_val, 'min': min_val})
                self.fields['product_id'].widget.attrs.update({'value': the_product.id})


def how_many_in_cart(the_product, username):
    user_cart = Order_Detail_Model.objects.filter(from_Main_order__owner__username=username, from_Main_order__is_paid=False, product=the_product)
    if user_cart.count() == 1:
        return user_cart.first().count
    else:
        return 0
