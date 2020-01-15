from django.shortcuts import render
from django.views import View
from django import http
from meiduo_mall.utils.response_code import RETCODE
from areas.models import Area
import logging
from django.core.cache import cache

logger = logging.getLogger('django')


# Create your views here.
class AreasView(View):
    def get(self, request):
        area_id = request.GET.get('area_id')
        # 如果前端没有传入area_id，表示用户需要省份数据
        if area_id is None:
            province_list = cache.get('province_list')
            if not province_list:
                try:
                    parent_model_list = Area.objects.filter(parent__isnull=True)
                    province_list = [{'id': parent_model.id, 'name': parent_model.name} for parent_model in
                                     parent_model_list]
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '身份数据错误'})
                cache.set('province_list', province_list, 3600)
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})

        # 如果前端传入了area_id，表示用户需要市或区数据
        else:
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    parent_model = Area.objects.get(id=area_id)  # 查询的模型
                    sub_model_list = parent_model.subs.all()
                    sub_list = [{'id': sub_model.id, 'name': sub_model.name} for sub_model in sub_model_list]
                    sub_data = {"id": parent_model.id, "name": parent_model.name, "subs": sub_list}
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '身份数据错误'})
                cache.set('sub_area_' + area_id, sub_data, 3600)
            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "OK", "sub_data": sub_data})
