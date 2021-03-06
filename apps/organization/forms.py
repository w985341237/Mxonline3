# ！/user/bin/python

# -_- coding:utf-8 -_-  # 编码格式

# @Time: 2019-02-18 15:43   # 文件生成时间

# @Author: Wangning   # 作者

# @File: forms.py   # 文件名

from django import forms
from operation.models import UserAsk
import re

# 普通的函数
# class UserAskForm(forms.Form):
#    name = forms.CharField(required=True,min_length=2,max_length=20)
#    mobile = forms.CharField(required=True,min_length=11,max_length=11)
#    course_name = forms.CharField(required=True,min_length=5,max_length=50)

# 进阶版函数


class UserAskForm(forms.ModelForm):
    # 除了继承现有的字段还可新增字段

    class Meta:
        model = UserAsk
        # 自定义需要验证的字段
        fields = ['name', 'mobile', 'course_name']

    # 验证手机号码是否合法
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
