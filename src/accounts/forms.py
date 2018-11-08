from django import forms
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
