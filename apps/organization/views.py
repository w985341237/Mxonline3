from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
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
                      'all_city': all_city,'all_orgs': orgs, 'org_nums': org_nums, 'city_id': city_id, 'category': category, 'hot_orgs': hot_orgs, 'sort': sort})


class OrgHomeView(View):
    pass

class AddAskView(View):
    pass
