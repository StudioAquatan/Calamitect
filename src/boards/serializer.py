from rest_framework import serializers

from .models import Good, Favorite, Comment


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ('user', 'article', 'created_at')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'article', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'image', 'user', 'article', 'created_at')
