from django.db.models import Q
from django.db import models
from django.http import Http404


class Product_Manager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id, active=True)
        if qs.count() == 1:
            return qs.first()
        else:
            raise Http404("محصول مورد نظر یافت نشد")

    # def get_by_slug(self, product_slug):
        # print(f"in get_by_slug >> slug is : {product_slug}")
        # qs = self.get_queryset().filter(slug=product_slug, active=True)
        # print(f"qs : {qs}")
        # if qs.count() == 1:
        #     return qs.first()
        # else:
        #     raise Http404("محصول مورد نظر یافت نشد")

    def get_by_categories(self, category_title):
        if category_title is None:
            raise Http404("صفحه مورد نظر یافت نشد")
        print(f"get by Category >>> {category_title}")
        # اینجا چون میخوایم از مدل categories که یک مدل هست فیلتر اعمال کنیم باید اسم و فیلدش رو بنویسیم
        qs = self.get_queryset().filter(categories__title__iexact=category_title, active=True)
        return qs

    def get_by_sub_categories(self, sub_category_title):
        if sub_category_title is None:
            raise Http404("صفحه مورد نظر یافت نشد")
        print(f"get by Category >>> {sub_category_title}")
        # اینجا چون میخوایم از مدل categories که یک مدل هست فیلتر اعمال کنیم باید اسم و فیلدش رو بنویسیم
        qs = self.get_queryset().filter(sub_categories__title__iexact=sub_category_title, active=True)
        return qs

    # حالا میخوایم Q بزاریم ینی فیلتر انجام بدیم تو دیتابین با OR
    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                # این زیری چون tag یک مدل هست پس باید فیلدش هم مشخص بشه بقیش از خودproduct هستن
                Q(tagsmodel__title__icontains=query)
        )

        return self.get_queryset().filter(lookup,  active=True).distinct()
    # distinct() اینو میزاریم برای وقتی که محصولی هم توی توضیحات و عنوان یه کلمه داشت دوبار نیارش
