from django.contrib import admin
from .models import TagsModel


class tags_admin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'slug']

    class Meta:
        model = TagsModel


# Register your models here.
admin.site.register(TagsModel, tags_admin)
