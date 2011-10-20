# Copyright 2011 Concentric Sky, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
