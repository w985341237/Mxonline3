from django import forms
# 引入验证码field
from captcha.fields import CaptchaField

# 登录表单验证


class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    # 此处的email与前端name需保持一致
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True,min_length=5)
    # 应用验证码
    captcha = CaptchaField()