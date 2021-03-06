from django import forms
# 引入验证码field
from captcha.fields import CaptchaField
from users.models import UserProfile

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
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField()


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码 自动以错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 忘记密码表单
class ForgetForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})

# 修改密码表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)

# 修改个人信息
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name","birthday","gender","address","mobile"]

# 用户头像修改
class ImageUploadForm(forms.ModelForm):
    # 除了继承现有字段，还可新增字段
    class Meta:
        model = UserProfile
        # 自定义需要验证的字段
        fields = ["image"]

# 邮箱验证码
class EmailCodeForm(forms.Form):
    email = forms.EmailField(required=True)


# 修改邮箱
class UpdateEmailForm(forms.Form):
    email = forms.EmailField(required=True)
    emailcode = forms.CharField(required=True,min_length=8,max_length=8)