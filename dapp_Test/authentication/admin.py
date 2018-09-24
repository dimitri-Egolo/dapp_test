# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from authentication.models import UserProfile
# Register your models here.


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)