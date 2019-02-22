from django.shortcuts import render
from django.views.generic import View
from course.models import Course
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from operation.models import UserFavorite
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        # 热门课程
        hot_courses = all_courses.order_by('-students')[:2]

        # 热门和参与人数排名
        sort = request.POST.get('sort','')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            if sort == 'students':
                all_courses = all_courses.order_by('students')

        # 对课程进行分页，尝试获取get请求传递过来的page参数
        # 如果不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_courses取出来，每页显示2个
        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)

        return render(request, 'course_list.html', {
                      'all_courses': courses, 'hot_courses': hot_courses})

# 课程详情
class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)

        # 用户查看点击查看课程详情，点击数应该+1
        course.click_nums += 1
        course.save()

        # 课程收藏
        has_fav_course = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True

        # 机构收藏
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        # 去除当前课程的标签
        tag = course.tag
        if tag:
            # 这里索引必须从1开始，否则会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[1:3]
        else:
            relate_courses = []

        return render(request,'course_detail.html',{'course':course,'relate_courses':relate_courses,'has_fav_course':has_fav_course,'has_fav_org':has_fav_org})

# 课程信息
class CourseInfoView(View):
    pass
