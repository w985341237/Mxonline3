from django.shortcuts import render
from django.views.generic import View
from course.models import Course
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        # 热门课程
        hot_courses = all_courses.order_by('fav_nums')[:5]

        # 对课程进行分页，尝试获取get请求传递过来的page参数
        # 如果不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_courses取出来，每页显示2个
        p = Paginator(all_courses, 2, request=request)

        courses = p.page(page)

        return render(request, 'course_list.html', {
                      'all_courses': courses, 'hot_courses': hot_courses})
