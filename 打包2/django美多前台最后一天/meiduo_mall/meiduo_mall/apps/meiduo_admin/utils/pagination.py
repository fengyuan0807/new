from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# /?page=2&pagesize=5


class StandardResultPagination(PageNumberPagination):
    page_size = 5
    # 指定获取分页数据时指定`页容量`的参数名称
    page_size_query_param = 'pagesize'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('counts', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))

