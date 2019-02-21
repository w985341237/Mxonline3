from django.db import models
from datetime import datetime
from organization.models import CourseOrg
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    DEGREE_CHOICES = (
        ('easy', u'初级'),
        ('middle', u'中级'),
        ('higher', u'高级')
    )
    degree = models.CharField(
        choices=DEGREE_CHOICES,
        max_length=6,
        verbose_name=u'难度',
    )
    # 后期会改用富文本
    detail = models.TextField(verbose_name='课程详情')
    # 使用分钟做后台记录（存储最小单位）前台转换
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数）')
    # 保存学习人数：点击开始学习才算
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(
        upload_to='courses/%Y/%m',
        verbose_name=u'封面图',
        max_length=100,
        blank=True
    )
    # 保存点击量，点进页面就算
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    course_org = models.ForeignKey(
        CourseOrg,
        on_delete=models.CASCADE,
        verbose_name='课程机构',
        blank=True,
        null=True,
    )
    # 课程标签
    tag = models.CharField(max_length=15,verbose_name=u'课程标签',default=u'')
    # 课程类别
    category = models.CharField(max_length=20,verbose_name=u'课程类别',default=u'后端开发')

    # 替代标签：course.lesson_set.count
    # 获取课程章节数
    #def get_zj_nums(self):
    #    return self.lesson_set.all().count()

    # 替代标签：course.usercourse_set.get_queryset|slice:":1"
    # 获取学习用户数，此处不用统计，我们只取前5个
    #def get_learn_users(self):
    #    return self.usercourse_set.all()[:5]

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 章节信息


class Lesson(models.Model):
    # 一个课程对应多个章节，在章节表中将课程设置为外键
    # 作为一个字段来存储让我们知道这个章节对应哪个课程
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    course = models.ForeignKey(
        'Course',
        verbose_name='课程',
        on_delete=models.CASCADE
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)

# 视频信息


class Video(models.Model):
    # 一个章节对应多个视频，在视频表中将章节设置为外键
    # 作为一个字段来存储让我们知道这个视频对应哪个章节
    lesson = models.ForeignKey(
        'Lesson',
        verbose_name=u'章节',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, verbose_name='视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 课程资源


class CourseResource(models.Model):
    # 一个课程对应很多资源，所以在课程资源中将课程设置为外键
    # 作为一个字段来存储让我们知道这个资源对应哪个课程
    course = models.ForeignKey(
        'Course',
        verbose_name=u'课程',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, verbose_name=u'名称')
    # 这里定义成文件类型的field，后台管理系统中会直接有上传的按钮
    # FileField也是一个字符串类型，要指定最大长度
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name=u'资源文件',
        max_length=200
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
