# -*- coding: utf-8 -*-

'''
Admin site for ifx

Created on 2019-02-05

@author: Aaron Kitzmiller <akitzmiller@g.harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College. All rights reserved.
@license: GPL v2.0
'''
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import AdminSite

User = get_user_model()


class IfxAdminSite(AdminSite):
    site_header = 'Ifx Portal'
    site_url = '/portal/'


admin_site = IfxAdminSite(name='ifxadmin')


class UserAdmin(admin.ModelAdmin):
    fields          = ('username', 'email', 'first_name', 'last_name', 'ifxid', 'is_staff', 'is_active', 'is_superuser')
    list_display    = ('username', 'email', 'first_name', 'last_name', 'ifxid', 'is_staff', 'is_active', 'is_superuser')
    list_filter     = ('is_staff', 'is_active', 'is_superuser')
    ordering        = ('-is_active', '-is_staff', 'last_name', 'first_name')
    search_fields   = ('username', 'email', 'first_name', 'last_name', 'ifxid', )


admin_site.register(get_user_model(), UserAdmin)

