from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django import http
from datetime import datetime
from django.utils import timezone
from .models import GoodsCategory, SKU, GoodsVisitCount
from .utils import get_categories, get_breadcrumb
from meiduo_mall.utils.response_code import RETCODE


# Create your views here.

class DetailVisitView(View):
    """商品访问量"""

    def post(self, request, category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id不正确')
        # 获取今天的日期,返回的时间对象
        t = timezone.localtime()
        today_str = "%d-%02d-%02d" % (t.year, t.month, t.day)
        # 时间字符串转事件对象
        today_date = datetime.strptime(today_str, '%Y-%m-%d')
        # 查询今天的访问量
        try:
            # 如果存在买直接获取记录对应的对象
            counts_data = GoodsVisitCount.objects.get(date=today_date, category=category)
        except GoodsVisitCount.DoesNotExist:
            # 如果不存在则新建对象
            counts_data = GoodsVisitCount()
        counts_data.category = category
        counts_data.count += 1
        counts_data.date = today_date
        try:
            counts_data.save()
        except Exception:
            return http.HttpResponseForbidden('统计失败')
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})


class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id不正确')
        # 商品分类
        categories = get_categories()
        # 面包屑
        breadcrumb = get_breadcrumb(sku.category)
        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context=context)


class HotGoodsView(View):
    """热销"""

    def get(self, request, category_id):
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price,
            })
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'hot_skus': hot_skus})


class ListView(View):
    """商品列表"""

    def get(self, request, category_id, page_num):
        # category_id 三级类别id
        try:
            # 获取三级类别
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('没有该类别')
        # 1\商品分类
        categories = get_categories()
        # 2\列表页面包屑导航
        # breadcrumb = {
        #     'cat1': category.parent.parent,
        #     'cat2': category.parent,
        #     'cat3': category,
        # }
        breadcrumb = get_breadcrumb(category)
        # 3\列表页分页和排序
        sort = request.GET.get('sort', 'default')  # 接收sort参数：如果用户不传，就是默认的排序规则
        # 按照商品创建时间排序
        # http: // www.meiduo.site: 8000 / list / 115 / 1 /?sort = default
        # 按照商品价格由低到高排序
        # http: // www.meiduo.site: 8000 / list / 115 / 1 /?sort = price
        # 按照商品销量由高到低排序
        # http: // www.meiduo.site: 8000 / list / 115 / 1 /?sort = hot
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-sales'
        else:
            sort = 'default'
            sort_field = 'create_time'
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)
        # 分页
        paginator = Paginator(object_list=skus, per_page=5)  # 数据是skus 每页显示5条数据
        # 获取当前页的商品数据
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return http.HttpResponseNotFound('empty page')
        total_page = paginator.num_pages
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sort': sort,
            'total_page': total_page,
            'page_skus': page_skus,
            'page_num': page_num,
            'category_id': category_id,
        }
        return render(request, 'list.html', context=context)
