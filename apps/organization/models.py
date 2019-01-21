from django.db import models
from datetime import datetime
# Create your models here.

# 课程机构


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    # 机构描述，后期会用富文本代替
    desc = models.TextField(verbose_name=u'机构描述')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name=u'封面图',
        max_length=100
    )
    course_numbers = models.IntegerField(default=0, verbose_name=u'课程数')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    # 一个城市可以有很多课程机构，将通过city设置外键，变成课程机构的一个字段
    # 可以让我们通过机构找到城市
    city = models.ForeignKey(
        'CityDict',
        verbose_name=u'所在城市',
        on_delete=models.CASCADE
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

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
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

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