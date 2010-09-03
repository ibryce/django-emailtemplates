from django.contrib import admin
from django import forms
from csky import admin as csky_admin
from emailtemplates.models import *


class RequiredContextItemInline(admin.TabularInline):
    model = RequiredContextItem
    extra = 1


class ModelTemplateAdmin(csky_admin.DefaultModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug', 'body')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'body')}),
    )
    inlines = (RequiredContextItemInline,)
#admin.site.register(ModelTemplate, ModelTemplateAdmin)


class EmailTemplateAdmin(csky_admin.DefaultModelAdmin):
    list_display = ('name', 'slug', 'subject', 'visible_from_address')
    search_fields = ('name', 'slug', 'subject', 'from_address', 'body')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'from_address')}),
        ('Body', {'fields': ('subject', 'body', 'txt_body')}),
    )
    inlines = (RequiredContextItemInline,)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
