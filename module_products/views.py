from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
from django.shortcuts import render
from module_SiteSettings.models import site_settings
from module_products.models import Product
from module_categories.models import ProductCategories, Product_SubCategories
from django.views.generic import ListView
from module_orders.forms import add_order_form
from module_product_comments.forms import ProductCommentsForm
from module_product_comments.models import Product_Comments_Model
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from termos_eshop.Utilities import giveme_cart, give_me_the_product_by_id
from termos_eshop.Utilities import is_ajax, bad_request_ajax_error


# ---------------------------------------------------------------- Categories View


# This class have to check again
class ProductsCategoriesView(ListView):
    template_name = "ProductsListLayout.html"
    paginate_by = 10

    def get_queryset(self):
        start_price, end_price, category_slug, sub_category_slug = 0, 0, None, None
        price_filter = False
        if is_ajax(self.request):
            self.template_name = "Component/AjaxProductsList.html"

            rolling: list = self.request.headers['Referer'].split('/products/')
            cat_names: list = rolling[1].split('/')
            if len(cat_names) == 1:
                category_slug = cat_names[0]
            elif len(cat_names) == 2:
                category_slug = cat_names[0]
                sub_category_slug = cat_names[1]
            else:
                raise Http404("درخواست نامعتبر")
            # Filter Process
            filter_price = self.request.GET.get('price_limit').split(' - ')
            start_price = int(filter_price[0].replace(',', ''))
            end_price = int(filter_price[1].replace(',', ''))
            price_filter = True

        else:
            try:
                category_slug = self.kwargs["main_category"]
            except KeyError:
                category_slug = None
            try:
                sub_category_slug = self.kwargs["sub_category"]
            except KeyError:
                sub_category_slug = None

        # --
        main_category = ProductCategories.objects.filter(slug=category_slug)

        header_cart, total_cart_price = giveme_cart(self.request)
        if main_category.count() > 0:
            main_category = main_category.first()
        else:
            raise Http404("صفحه مورد نظر یافت نشد")

        all_categories: ProductCategories = ProductCategories.objects.all()
        s_settings = site_settings.objects.first()
        self.extra_context = {
            'site_settings': s_settings,
            'main_category': main_category,
            'category_bar': all_categories,
            'found_product_count': Product.objects.get_by_categories(category_title=main_category.title).count(),
            'header_cart': header_cart,
            'total_cart_price': total_cart_price,
        }

        base_products = Product.objects.get_by_categories(category_title=main_category.title)
        if sub_category_slug is not None:

            # sub Category Start:
            sub_category = Product_SubCategories.objects.filter(slug__exact=sub_category_slug)
            if sub_category.count() > 0:
                sub_category = sub_category.first()
                self.extra_context['sub_category'] = sub_category
                base_products = Product.objects.get_by_sub_categories(sub_category_title=sub_category.title)
                self.extra_context['found_product_count'] = base_products.count()
            else:
                raise Http404("صفحه مورد نظر یافت نشد")
            # sub Category END:

        # Category Start:
        if base_products.count() > 0:
            self.extra_context['db_max_price'] = base_products.order_by('-price').first().price
        else:
            self.extra_context['db_max_price'] = 0

        if not price_filter:
            return base_products
        else:
            final_query = base_products.filter(price__gte=start_price, price__lte=end_price)
            self.extra_context['found_product_count'] = final_query.count()
            self.extra_context['filter_view'] = True
            self.extra_context['start_price'] = start_price
            self.extra_context['end_price'] = end_price
            return final_query


# (-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-) SEARCH AND TAG VIEW (-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)
# (-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-) SEARCH AND TAG VIEW (-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)

class Products_SearchAndTag_View(ListView):
    template_name = "ProductsListLayout.html"
    paginate_by = 10

    def get_queryset(self):

        query = self.request.GET.get('q')  # search-query request
        # s_settings = site_settings.objects.first()
        # all_categories: ProductCategories = ProductCategories.objects.all()
        # main_order_cart = giveme_cart(self.request)
        self.extra_context = {
            # 'main_order_cart': main_order_cart,
            # 'site_settings': s_settings,
            'main_category': query,
            # 'category_bar': all_categories,
            'found_product_count': 0,
            # 'is_it_in_search': True,
            'q': query,
        }

        # lvl.1 : Filter products according to requested q "search"
        if (query is not None) and (query != 'None'):
            found_products = Product.objects.search(query)
        else:
            # if search-query is not requested then > found_products = all active products
            found_products = Product.objects.get_active_products()

        # category filter
        try:
            category_slug = self.kwargs["main_category"]
        except KeyError:
            category_slug = None
        try:
            sub_category_slug = self.kwargs["sub_category"]
        except KeyError:
            sub_category_slug = None

        sub_category = Product_SubCategories.objects.filter(slug=sub_category_slug)
        main_category = ProductCategories.objects.filter(slug=category_slug)

        if sub_category.count() > 0:
            sub_category = sub_category.first()
        else:
            sub_category = None
        if main_category.count() > 0:
            main_category = main_category.first()
        else:
            main_category = None

        self.extra_context['sub_category'] = sub_category
        self.extra_context['main_category'] = main_category

        if sub_category:
            found_products = Product.objects.filter(sub_categories=sub_category)
        elif main_category:
            found_products = Product.objects.filter(categories=main_category)

        if found_products:
            self.extra_context['db_max_price'] = found_products.order_by('-price').first().price
        else:
            self.extra_context['db_max_price'] = 0

        # process the sort request
        try:
            sort_req = self.request.GET.get('sort_order')
            if sort_req is not None:
                if sort_req == 'cheapest-tab':
                    found_products = found_products.order_by('price')
                    self.extra_context['sort_order'] = "cheapest-tab"
                elif sort_req == 'most-expensive-tab':
                    found_products = found_products.order_by('-price')
                    self.extra_context['sort_order'] = "most-expensive-tab"
                elif sort_req == 'newest-tab':
                    found_products = found_products.order_by('-added_date')
                    self.extra_context['sort_order'] = "newest-tab"
        except KeyError:
            pass

        # check the filter-request (it comes with ajax request)
        if is_ajax(self.request):
            self.template_name = "Component/AjaxProductsList.html"
            self.extra_context['filter_view'] = True
            # price filter
            filter_price = self.request.GET.get('price_limit').split(' - ')
            start_price = int(filter_price[0].replace(',', ''))
            end_price = int(filter_price[1].replace(',', ''))
            self.extra_context['start_price'] = start_price
            self.extra_context['end_price'] = end_price
            found_products = found_products.filter(price__gte=start_price, price__lte=end_price)
        else:
            self.extra_context['filter_view'] = False

        # هیچ درخواستی برای فیلتر قیمت نداریم
        if found_products.count() > 0:
            self.extra_context['found_product_count'] = found_products.count()
        else:
            self.extra_context['found_product_count'] = 0
        return found_products


# ---------------------------------------------------------------- Detail View

def product_detail_view(req, p_id, **kwargs):
    the_product = give_me_the_product_by_id(p_id)
    if the_product is None:
        raise Http404("محصول مورد نظر یافت نشد")
    the_product.visit_counter += 1
    the_product.save()
    the_user = req.user if req.user.is_authenticated else None
    s_settings = site_settings.objects.first()

    # start from here ------------------

    # 1. get quantity of product in the user's cart
    main_order_cart = giveme_cart(req)
    found_product_quantity = main_order_cart.get_amount_of_product_in_cart(the_product=the_product)

    # 2. find the categories of product for showing category links
    main_category = ProductCategories.objects.filter(product=the_product)
    main_category = main_category.first() if main_category.count() else None
    sub_category = Product_SubCategories.objects.filter(product=the_product)
    sub_category = sub_category.first() if sub_category.count() else None

    # 3. new order_form
    # اینشیال ها رو اگر با نام فیلد تغییر بدیم والیو اون فیلد تغییر میکنه اگر نه باید توی فرم آپدیت بزنی
    order_form = add_order_form(req.POST or None, initial={
        'the_product': the_product, 'found_product_count': found_product_quantity})
    # مثلا این زیری رو اگر بزنی توی هر محصولی که بری مقدار فیلد (انتخاب تعداد برای اضافه کردن به سبد خرید ) رو برابر با p_id میکنه ینی
    # فیلد order_count رو مقدار value رو برابر p_id میکنه
    # order_form = add_order_form(req.POST or None, initial={'product_id': product.id, 'order_count': p_id})

    cont = {
                'site_settings': s_settings,  # to show free limit shipping on the page (free shipping over ..$)
                'main_category': main_category,
                'sub_category': sub_category,
                'found_product_count': found_product_quantity,
                'the_product': the_product,
                'order_form': order_form,
                'GOOGLE_SITE_KEY': settings.GOOGLE_SITE_KEY,
            }

    # if sub_category is not None:
    #     cont['found_product_count'] = Product.objects.get_by_sub_categories(sub_category.title).count()

    # -------------------- Comments
    lookup = (Q(is_accepted=True) | Q(owner=the_user))
    cont['product_comments'] = Product_Comments_Model.objects.filter(lookup, product_id=p_id).order_by('-created_date')
    cont['comment_form'] = ProductCommentsForm

    # cont['total_cart_price'] = "{:,}".format(int(cont['total_cart_price']))
    return render(req, "ProductDetailLayout.html", cont)


# -----------------------------------------------  AJAX Add WISHLIST  -----------------------------------------------
# -----------------------------------------------  AJAX Add WISHLIST  -----------------------------------------------


def ajax_wishlist(req):  # 11/7/2022 m/d/y

    data = {}
    if is_ajax(req):
        try:
            product_id = req.POST['p_id']
        except KeyError:
            return bad_request_ajax_error()
        the_product = give_me_the_product_by_id(product_id)

        if the_product:
            if req.user.is_authenticated:
                req_from_dashboard = str(req.headers['Referer']).endswith(reverse("module_profile:urls_profile_view"))
                req_from_wishlist_page = str(req.headers['Referer']).endswith(reverse("module_profile:urls_profile_wishlist"))

                the_product_in_wishlist = the_product.wisher_users.filter(id=req.user.id)

                if the_product_in_wishlist.count() == 0:  # if the product is not in user's wishlist
                    # add it
                    the_product.wisher_users.add(req.user)
                    data['add_remove'] = 'added'
                    if req_from_dashboard:  # if the request came from dashboard_page > send rendered wishlist_Layout
                        cont = {'wish_list': Product.objects.filter(wisher_users=req.user)}
                        data['outer'] = render_to_string("profile/ProfileLayout/DashboardWishlistLayout.html", cont)
                    return JsonResponse(data, status=200)
                else:  # user already has the product _ or anything else
                    # remove
                    the_product.wisher_users.remove(req.user)
                    data['add_remove'] = 'removed'
                    if req_from_dashboard:  # if the request came from dashboard_page > send rendered wishlist_Layout
                        cont = {'wish_list': Product.objects.filter(wisher_users=req.user)}
                        data['outer'] = render_to_string("profile/ProfileLayout/DashboardWishlistLayout.html", cont)
                    if req_from_wishlist_page:  # if the user removed product from wishlist page
                        cont = {'wish_list': Product.objects.filter(wisher_users=req.user)}
                        data['outer'] = render_to_string("profile/Wishlist/wishlist_items.html", cont)
                    return JsonResponse(data, status=200)
            else:
                # user is not logged in > goto Login Page
                data['add_remove'] = 'login'

                try:
                    next_page = str(req.headers['Referer'])
                    next_page = next_page.replace(str(req.headers['Origin']), '?next=')
                except KeyError:
                    next_page = ''

                data['login_url'] = reverse("module_users:urls_Login_Page") + next_page
                return JsonResponse(data, status=200)

        else:
            return bad_request_ajax_error()
