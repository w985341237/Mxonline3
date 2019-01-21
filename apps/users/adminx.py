import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner

# 创建admin的管理类，这里不再是继承admin，而是继承object


# 邮箱验证码后台管理器


class EmailVerifyRecordAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 配置搜索字段，不做时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 轮播图后台管理器


class BannerAdmin(object):
    # 配置后台显示列
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 配置后台搜索字段
    search_fields = ['title', 'image', 'index', 'url']
    # 配置筛选字段
    list_filter = ['title', 'image', 'index', 'url', 'add_time']


# 创建xadmin的全局管理器并与view绑定


class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# xadmin全局配置参数信息设置


class GlobalSetting(object):
    site_title = '王宁：慕课后台管理站'
    site_footer = "wangning's mooc"
    # 收起菜单
    menu_style = "accordion"


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 头部与脚步信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSetting)
