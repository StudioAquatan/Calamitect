import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def get_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Article(models.Model):
    """
    記事のモデル
    """
    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    category_type = models.IntegerField(verbose_name=_("category"), default=0)
    image = models.ImageField(verbose_name=_("image"), upload_to=get_image_path)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"))


class Tag(models.Model):
    """
    記事につけるタグのモデル
    """
    name = models.CharField(verbose_name=_("tag"), max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("article"))


class Good(models.Model):
    """
    いいねのモデル
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("article"))
    created_at = models.DateTimeField(_("date_created"), auto_now_add=True)


class Favorite(models.Model):
    """
    ユーザの記事に対するお気に入りのモデル
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=_("favorite"),
                             verbose_name=_("user"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name=_("favorite"),
                                verbose_name=_("article"))
    created_at = models.DateTimeField(_("date_created"), auto_now_add=True)


class Comment(models.Model):
    """
    コメントのモデル
    """
    text = models.CharField(verbose_name=_("text"), max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=_("comments"),
                             verbose_name=_("user"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name=_("comments"),
                                verbose_name=_("article"))
    created_at = models.DateTimeField(_("date_created"), auto_now_add=True)
