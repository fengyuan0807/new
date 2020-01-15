from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


# 订单序列化器类
class OrderInfoSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(label='创建时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image')


class OrderGoodsSerializer(serializers.ModelSerializer):
    # 关联序列嵌套SKU的序列化器类 多对一
    sku = SKUSerializer(label='SKU')

    class Meta:
        model = OrderGoods
        fields = ('id', 'count', 'price', 'sku')


# 订单详情序列化器类
class OrderInfoDetailSerializer(serializers.ModelSerializer):
    # 关联序列嵌套OrderGoods的序列化器类 一对多 加many=True
    skus = OrderGoodsSerializer(label='订单商品', many=True)
    create_time = serializers.DateTimeField('%Y-%m-%d %H:%M:%S', label='创建时间')
    user = serializers.StringRelatedField(label='下单的用户')

    class Meta:
        model = OrderInfo
        exclude = ('address', 'update_time')


# 修改订单状态
class OrderInfoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')
        extra_kwargs = {
            'order_id': {
                'read_only': True
            }
        }
