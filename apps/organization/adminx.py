import xadmin

from .models import CourseOrg, Teacher, CityDict


# 课程机构后台管理器


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','category', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc','category', 'click_nums', 'fav_nums']
    list_filter = [
        'name',
        'desc',
        'category',
        'click_nums',
        'fav_nums',
        'city__name',
        'add_time']

    # 搜索框，当课程数量过大时，有课程指向他，会以ajax方式加载
    relfield_style = 'fk-ajax'


# 讲师后台管理器


class TeacherAdmin(object):
    list_display = [
        'name',
        'work_position',
        'work_years',
        'work_company',
        'click_nums',
        'fav_nums',
        'org']
    search_fields = [
        'name',
        'work_position',
        'work_years',
        'work_company',
        'click_nums',
        'fav_nums',
        'org']
    list_filter = [
        'name',
        'work_position',
        'work_years',
        'work_company',
        'click_nums',
        'fav_nums',
        'org__name']


# 城市信息后台管理器


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
