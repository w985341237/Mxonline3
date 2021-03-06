import xadmin
from .models import Course, Lesson, Video, CourseResource

# 课程直接添加章节
class LessonInline(object):
    model = Lesson
    extra = 0

# 课程直接添加资源
class ResourceInline(object):
    model = CourseResource
    extra = 0


# 课程后台管理器


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
    # 字段显示样式
    style_fields = {'detail':'ueditor'}

    # 默认排序：以点击数排序
    ordering = ['-click_nums']

    # 字段只读：点击数只允许读取
    readonly_fields = ['click_nums','fav_nums']

    # 字段隐藏：收藏数隐藏显示
    exclude = ['fav_nums']

    # 课程直接添加章节,资源
    inlines = [LessonInline,ResourceInline] # 数组，支持多个

    # 直接列表页编辑
    list_editable = ['degree','desc']

    # 列表定时刷新3s或者5s
    refresh_times = 3,5


# 章节后台管理器


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']

    # __name代表使用外键中name字段
    list_filter = ['name', 'course__name', 'add_time']


# 视频后台管理器


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


# 课程资源后台管理器


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course__name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
