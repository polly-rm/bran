from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.db import models


class CustomFlatPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    search_fields = ['title', 'content',]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
