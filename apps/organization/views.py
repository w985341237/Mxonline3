from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from organization.models import CityDict, CourseOrg, Teacher
from course.models import Course
from operation.models import UserFavorite
from pure_pagination import Paginator, PageNotAnInteger
from organization.forms import UserAskForm
# Create your views here.

# 课程机构列表功能


class OrgView(View):
    def get(self, request):
        # 查找所有城市信息
        all_city = CityDict.objects.all()

        # 查找所有课程机构信息
        all_orgs = CourseOrg.objects.all()

        city_id = request.GET.get('city', '')
        # 选中了某个城市之后，根据城市的ID与数据库中的city_id进行判断，（外键city在数据库中名为city_id且为字符串类型）
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别的筛选
        # ct是我们前端页面用于判断类别用的
        category = request.GET.get('ct', '')
        # 选中了类别之后，根据category与数据库中的category进行判断，从而显示授课机构
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 统计课程机构的数量
        org_nums = all_orgs.count()

        # 授课机构的排名,取前三个
        hot_orgs = all_orgs.order_by('click_nums')[:3]

        # 学习人数和课程人数排名
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            if sort == 'courses':
                all_orgs = all_orgs.order_by('-courses')

        # 对课程机构进行分页，尝试获取前端get请求传递过来的page参数
        # 如果是不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_orgs中取出来，每页显示6个，这个字段必填
        p = Paginator(all_orgs, 6, request=request)
        orgs = p.page(page)

        return render(request, 'org_list.html', {
                      'all_city': all_city, 'all_orgs': orgs, 'org_nums': org_nums, 'city_id': city_id, 'category': category, 'hot_orgs': hot_orgs, 'sort': sort})

# 机构首页


class OrgHomeView(View):
    def get(self, request, org_id):
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 当前机构所有课程,取4个
        all_courses = course_org.course_set.all()[:4]

        # 当前机构所有讲师，取两个
        all_teachers = course_org.teacher_set.all()[:2]

        current_page = 'home'

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current_page':current_page,
            'has_fav':has_fav,
        })

# 机构详情页


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))

        current_page = 'desc'

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html',
                      {'course_org': course_org,'current_page':current_page,'has_fav':has_fav})


# 机构讲师页
class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        current_page = 'teacher'

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html',
                      {'course_org':course_org,'all_teachers': all_teachers,'current_page':current_page,'has_fav':has_fav})


# 机构课程页
class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        current_page = 'course'

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',
                      {'course_org':course_org,'all_courses': all_courses,'current_page':current_page,'has_fav':has_fav})


class AddAskView(View):
    # 用户添加咨询
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        # 判断form是否有效
        if userask_form.is_valid():
            #  注意modelform和form的区别，modelform它有model的属性，而且有个参数commit，当它为真时会把数据存入到数据库
            user_ask = userask_form.save(commit=True)

            # 如果保存成功,则返回json,不过后面必须有content_type用于告诉浏览器返回的类型
            return HttpResponse("{'status':'success'}",
                                content_type='application/json')
        else:
            # 如果保存失败，则返回json,并将form的错误信息通过msg传递到前端进行显示
            return HttpResponse(
                "{'status':'fail','msg':'您输入的字段有错误'}", content_type='application/json')

# 用户收藏与取消收藏


class AddFavView(View):
    def post(self,request):
        # 取出fav_id，尽管是字符串类型，后期我们会转换为整型，所以默认为0
        fav_id = request.POST.get('fav_id',0)
        # 取出fav_type，尽管是字符串类型，后期我们会转换为整型，所以默认为0
        fav_type = request.POST.get('fav_type',0)

        # 未收藏时收藏和已收藏时取消
        # 判断用户是否登录，及时用户没有登录会有一个匿名的user
        if not request.user.is_authenticated:
            # 未登录时提示未登录，并跳转到登录界面
            return HttpResponse({'status':'fail','msg':'用户还未登陆'},content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=fav_type)
        if exist_records:
            # 如果记录已经存在，那么用户可以取消收藏
            exist_records.delete()
            # 下面是根据收藏类型来进行删除，同时删除后机构类型对应的喜欢人数也会-1
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse({'status':'success','msg':'收藏'},content_type='application/json')
        else:
            # 实例化一个对象
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                # 保存到数据库
                user_fav.save()
                # 下面是根据收藏类型来进行增加，同时增加记录后机构对应的喜欢人数也会+1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse({'status':'success','msg':'已收藏'},content_type='application/json')
            else:
                # 收藏出错
                return HttpResponse({'status':'fail','msg':'收藏出错'},content_type='application/json')