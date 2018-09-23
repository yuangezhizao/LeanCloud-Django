from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(
        attrs={'class': 'ui left icon input', 'placeholder': '请输入用户名', 'autofocus': ''}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'ui left icon input', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'ui left icon input', 'placeholder': '请再次输入密码'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'ui left icon input', 'placeholder': '请输入邮箱'}))
    sex = forms.ChoiceField(label='性别',
                            choices=gender)  # widget=forms.Select(attrs={'class': 'ui dropdown selection multiple'}),
    captcha = CaptchaField(label='验证码')
    # agree_toc = forms.BooleanField(required=True, label='我同意用户协议')
