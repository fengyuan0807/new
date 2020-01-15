from django.views import View
from django import http

from goods.models import GoodsCategory, SKU


class HotGoodsView(View):
    def get(self, request, category_id):
        # try:...
        category = GoodsCategory.objects.get(id=category_id)
        # 一对多
        skus = category.sku_set.filter(is_launched=True).order_by('sales')[0:2]
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })
        return http.JsonResponse({'code': 'OK', 'errmsg': 'ok', 'hot_skus': hot_skus})
