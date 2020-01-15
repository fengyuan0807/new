# category 查询 sku 一查多
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage

from goods.models import GoodsCategory, SKU


class ListView(View):
    def get(self, request, category_id, page_num):
        sort = request.GET.get('sort', 'default')
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = 'sales'
        else:
            sort = 'default'
            sort_field = 'create_time'
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoseNotExist:
            return http.HttpResponseForbidden('...')
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)
        # skus = SKU.objects.filter(category=category,is_launched=True)
        paginator = Paginator(skus, 5)
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            return http.HttpResponseForbidden('empty page')
        total_page = paginator.num_pages
        # skus  total_page page_num sort page_skus