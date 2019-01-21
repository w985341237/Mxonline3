import xadmin
from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'degree',
        'detail',
        'learn_times',
        'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'students']


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']

    # __name代表使用外键中name字段
    list_filter = ['name', 'course__name', 'add_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course__name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
