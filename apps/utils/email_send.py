# encoding = utf-8
from random import Random

from users.models import EmailVerifyRecord
# 导入Django自带的邮件模块
from django.core.mail import send_mail
# 导入setting中发送邮件的配置
from Mxonline3.settings import EMAIL_FROM

# 生成随机字符串
def random_str(random_lenth=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    lenth = len(chars) - 1
    random = Random()
    for i in range(random_lenth):
        # 从chars里按索引随机取值
        str += chars[random.randint(0,lenth)]
    return str

# 发送注册邮件
def send_register_email(email,send_type='register'):
    # 发送之前先保存到数据库，到时候查询链接是否存在

    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容：
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'wangning慕课小站 注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        # 使用Django内置函数完成邮件的发送。四个参数：主题，邮件内容，从哪里发，接收者list
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        # 如果发送成功
        if send_status:
            pass

    # 登录页忘记密码
    elif send_type == 'forget':
        email_title = 'wangning慕课小站 重置密码链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    # 个人中心修改密码
    elif send_type == 'update_email':
        email_title = 'wangning慕课小站 修改密码验证码'
        email_body = '您的验证码为: http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
