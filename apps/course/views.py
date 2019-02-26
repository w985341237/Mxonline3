from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from course.models import Course, CourseResource,Video
from operation.models import UserCourse, CourseComments
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from operation.models import UserFavorite
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        # 热门课程
        hot_courses = all_courses.order_by('-students')[:2]

        # 热门和参与人数排名
        sort = request.POST.get('sort', '')
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
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)

        # 用户查看点击查看课程详情，点击数应该+1
        course.click_nums += 1
        course.save()

        # 课程收藏
        has_fav_course = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

        # 机构收藏
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.id, fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        # 去除当前课程的标签
        tag = course.tag
        if tag:
            # 这里索引必须从1开始，否则会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[1:3]
        else:
            relate_courses = []

        return render(request, 'course_detail.html', {
                      'course': course, 'relate_courses': relate_courses, 'has_fav_course': has_fav_course, 'has_fav_org': has_fav_org})

# 课程章节信息


class CourseInfoView(LoginRequiredMixin, View):
    # 如果用户没有登录，是不能进来该界面，装饰器loginrequired会让其跳转到登录页面
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        # 该课程所有资源
        all_resources = CourseResource.objects.filter(course=course)

        # 取出所有选过这门课的学生
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有选过这门课的学生的id，采用递归表达式形式
        user_ids = [user_course.user_id for user_course in user_courses]
        # 取出刚才那些学生选过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出刚才那些学生选过的所有的课程的id,同样采用递归的表达式形式
        course_ids = [
            all_user_course.course_id for all_user_course in all_user_courses]
        # 取出学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(
            id__in=course_ids).order_by('-click_nums')

        # 查询用户是否已经开始学习了该课程，如果没有则开始学习
        user_course = course.usercourse_set.filter(
            user=request.user, course=course)
        if not user_course:
            # 进入该界面，课程学习人数+1
            course.students += 1
            # 机构学生+1
            course.course_org.students += 1
            course.save()
            # 用户课程
            usercourse = UserCourse()
            usercourse.course = course
            usercourse.user = request.user
            usercourse.save()

        return render(request, 'course_video.html', {
                      'course': course, 'relate_courses': relate_courses, 'all_resources': all_resources})


# 课程评论

class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        all_comments = CourseComments.objects.all()
        all_recources = CourseResource.objects.filter(course=course)

        # 取出所有选过这门课的学生
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有选过这门课的学生的id，采用递归表达式形式
        user_ids = [user_course.user_id for user_course in user_courses]
        # 取出刚才那些学生选过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出刚才那些学生选过的所有的课程的id,同样采用递归的表达式形式
        course_ids = [
            all_user_course.course_id for all_user_course in all_user_courses]
        # 取出学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(
            id__in=course_ids).order_by('-click_nums')

        return render(request, 'course_comment.html', {
                      'course': course, 'all_comments': all_comments,
                      'all_resources': all_recources, 'relate_courses': relate_courses})

# 增加课程评论


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(
                "{'status':'fail','msg':'用户未登录'}", content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # get方法只能取出一条数据，如果有多条则抛出异常而且没有数据也抛异常
            # filter方法可以取一个列表出来（可以遍历的queryset），没有数据返回空的queryset，是不会抛异常的
            course = Course.objects.get(pk=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(
                "{'status':'success,'msg':'评论成功}", content_type='application/json')
        else:
            return HttpResponse(
                "{'status':'fail','msg':'评论失败'}", content_type='application/json')


# 视频播放

class VideoPlayView(View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self,request,video_id):
        video = Video.objects.get(pk=video_id)
        course = video.lesson.course

        # 取出所有选过这门课的学生
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有选过这门课的学生的id，采用递归表达式形式
        user_ids = [user_course.user_id for user_course in user_courses]
        # 取出刚才那些学生选过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出刚才那些学生选过的所有的课程的id,同样采用递归的表达式形式
        course_ids = [
            all_user_course.course_id for all_user_course in all_user_courses]
        # 取出学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(
            id__in=course_ids).order_by('-click_nums')

        return render(request,'course_play.html',{'video':video,'course':course,'relate_courses':relate_courses})
