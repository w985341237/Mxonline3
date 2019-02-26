# ！/user/bin/python

# -_- coding:utf-8 -_-  # 编码格式

# @Time: 2019-02-26 09:55   # 文件生成时间

# @Author: Wangning   # 作者

# @File: mixin_utils.py   # 文件名

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
