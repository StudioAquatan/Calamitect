from django import forms

from .models import Article


class CreateArticleForm(forms.ModelForm):
    """ 記事投稿用のフォーム """

    class Meta:
        model = Article
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'タイトル',
            'description': '本文',
            'image': '画像'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['title'].widget.attrs = {'placeholder': 'title'}
        self.fields['image'].required = False
        self.fields['description'].required = True
        self.fields['description'].widget.attrs = {'placeholder': 'description'}

    def clean(self):
        super().clean()
