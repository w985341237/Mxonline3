import xadmin

from .models import CourseOrg,Teacher,CityDict


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','add_time']
    search_fields = ['name','desc','click_nums','fav_nums']
    list_filter = ['name','desc','click_nums','fav_nums','city__name','add_time']


class TeacherAdmin(object):
    list_display = ['name','work_position','work_years','work_company','click_nums','fav_nums','org']
    search_fields = ['name','work_position','work_years','work_company','click_nums','fav_nums','org']
    list_filter = ['name','work_position','work_years','work_company','click_nums','fav_nums','org__name']


class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']


xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CityDict,CityDictAdmin)