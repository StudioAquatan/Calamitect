from django import forms
from django.contrib.auth.forms import UsernameField

from .models import User


class RegisterUserForm(forms.ModelForm):
    """ ユーザ登録画面用のフォーム """

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_icon', 'password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'password'}),
        }

    confirm_password = forms.CharField(
        label='確認用パスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'password (again)'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'username'}
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'e-mail'}

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")


class LoginUserForm(forms.Form):
    """ログイン画面用のフォーム"""

    username = UsernameField(
        label='Username',
        max_length=255,
    )

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError(
                '%(min_length)s 文字以上で入力してください', params={'min_length': 3}
            )
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しいユーザ名を入力してください")
        if not user.check_password(password):
            raise forms.ValidationError("正しいパスワードを入力してください")

    def get_user(self):
        username = self.cleaned_data.get('username')
        user = User.objects.get(username=username)
        return user
