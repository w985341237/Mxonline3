# encoding : utf-8
from django.db import models
from datetime import datetime
# Create your models here.

# 课程机构


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    # 机构描述，后期会用富文本代替
    desc = models.TextField(verbose_name=u'机构描述')
    # 机构类别
    ORG_CHOICES = (
        ('pxjg',u'培训机构'),
        ('gx',u'高校'),
        ('gr',u'个人')
    )
    category = models.CharField(max_length=20,choices=ORG_CHOICES,verbose_name=u'机构类别',default='pxjg')
    tag = models.CharField(max_length=10,default=u'国内名校',verbose_name=u'机构标签')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name=u'封面图',
        max_length=100,
        blank=True
    )
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    # 一个城市可以有很多课程机构，将通过city设置外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(
        'CityDict',
        verbose_name=u'所在城市',
        on_delete=models.CASCADE
    )
    # 当学生点击学习课程，找到所数机构，学习人数+1
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    # 当发布课程就+1
    course_numbers = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '课程机构：{0}'.format(self.name)

# 讲师


class Teacher(models.Model):
    org = models.ForeignKey(
        'CourseOrg',
        verbose_name=u'所属机构',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职位')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    age = models.IntegerField(default=18,verbose_name=u'年龄')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    image = models.ImageField(
        upload_to='teacher/%Y/%m',
        default='image/default.png',
        verbose_name=u'头像',
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = u'机构讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}讲师：{1}'.format(self.org,self.name)


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    # 城市描述：备用，不一定展示出来
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name