import os
import uuid

from django.contrib.auth.models import User
from django.db import models

from src.calamitect.settings import MEDIA_ROOT


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


def delete_previous_file(function):
    """不要となる古いファイルを削除する為のデコレータ実装.

    :param function: メイン関数
    :return: wrapper
    """

    def wrapper(*args, **kwargs):
        """Wrapper 関数.

        :param args: 任意の引数
        :param kwargs: 任意のキーワード引数
        :return: メイン関数実行結果
        """
        self = args[0]

        # 保存前のファイル名を取得
        result = Article.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Article, self).save()

        # 関数実行
        result = function(*args, **kwargs)

        # 保存前のファイルがあったら削除
        if previous:
            os.remove(MEDIA_ROOT + '/' + previous.image.name)
        return result

    return wrapper


class Article(models.Model):
    """
    記事のモデル
    """

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Article, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Article, self).delete()

    title = models.CharField(verbose_name="タイトル", max_length=255)
    description = models.TextField(verbose_name="本文")
    category_type = models.IntegerField(verbose_name="カテゴリー", default=0)
    image = models.ImageField(verbose_name="画像", upload_to=get_image_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")


class Tag(models.Model):
    """
    記事につけるタグのモデル
    """
    name = models.CharField(verbose_name="タグ", max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="記事")


class Good(models.Model):
    """
    いいねのモデル
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="記事")
    created_at = models.DateTimeField("お気に入りした日時", auto_now_add=True)
