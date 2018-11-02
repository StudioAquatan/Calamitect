from django.contrib import admin

from . import models


class UserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "is_staff")


admin.site.register(models.User, UserModelAdmin)
