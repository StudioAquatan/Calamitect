from django.contrib import admin

from . import models


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category_type", "user")


class TagModelAdmin(admin.ModelAdmin):
    list_display = ("name",)


class GoodModelAdmin(admin.ModelAdmin):
    list_display = ("article", "user")


class FavoriteModelAdmin(admin.ModelAdmin):
    list_display = ("article", "user")


admin.site.register(models.Article, ArticleModelAdmin)
admin.site.register(models.Tag, TagModelAdmin)
admin.site.register(models.Good, GoodModelAdmin)
admin.site.register(models.Favorite, FavoriteModelAdmin)
