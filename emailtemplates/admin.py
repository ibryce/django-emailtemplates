from django.contrib import admin
from django import forms
from csky.admin import UserModelAdmin
from csky.widgets import WYMEditor
from emailtemplates.models import *


class RequiredContextItemInline(admin.TabularInline):
  model = RequiredContextItem
  extra = 1

class ModelTemplateAdminForm(forms.ModelForm):
  class Meta:
    model = ModelTemplate
  body = forms.CharField(widget=WYMEditor())

class ModelTemplateAdmin(UserModelAdmin):
  list_display = ('name','slug')
  search_fields = ('name','slug','body')
  form = ModelTemplateAdminForm
  fieldsets = (
    (None,  {'fields': ('name','slug','body')}),
  )
  inlines = (RequiredContextItemInline,)
#admin.site.register(ModelTemplate, ModelTemplateAdmin)

class EmailTemplateAdminForm(forms.ModelForm):
  class Meta:
    model = EmailTemplate
  body = forms.CharField(widget=WYMEditor())

class EmailTemplateAdmin(UserModelAdmin):
  list_display = ('name','slug','visible_from_address')
  search_fields = ('name','slug','from_address','body')
  form = EmailTemplateAdminForm
  fieldsets = (
    (None,  {'fields': ('name','slug','from_address')}),
    ('Body', {'fields': ('subject','body','txt_body')}),
  )
  inlines = (RequiredContextItemInline,)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
