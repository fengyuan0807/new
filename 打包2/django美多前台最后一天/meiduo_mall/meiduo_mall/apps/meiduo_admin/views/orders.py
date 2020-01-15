from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrderInfoSerializer, OrderInfoDetailSerializer, OrderInfoStatusSerializer
from orders.models import OrderInfo


class OrdersViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            # 订单关联的订单商品记录中关联的sku商品的名称中含有关键字
            # orderinfo.skus.all()
            # 取其中的一个orderinfo.skus.all()[0].sku.name
            orderinfos = OrderInfo.objects.filter(Q(order_id=keyword) |
                                                  Q(skus__sku__name__contains=keyword)).distinct()
        else:
            orderinfos = OrderInfo.objects.all()
        return orderinfos

    # serializer_class = OrderInfoSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = OrderInfoSerializer

        elif self.action == 'retrieve':
            serializer_class = OrderInfoDetailSerializer
        else:
            serializer_class = OrderInfoStatusSerializer
        return serializer_class

    # get ---> list
    # def list(self, request, *args, **kwargs):
    #     orderinfos=self.get_queryset()
    #     serializer = self.get_serializer(orderinfos, many=True)
    #     return Rseponse(serializer.data)
    # 订单详情获取
    #  get ---> retrieve
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    # 订单状态修改
    # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/
    @action(methods=['put'], detail=True)
    # def status(self, request, pk):
    #     orderinfo = self.get_object()
    #     serializer = self.get_serializer(orderinfo, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=201)
    def status(self, request, pk):
        return self.update(request, pk)
