from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(label='商品频道组名称')
    category = serializers.StringRelatedField(label='商品的一级分类')

    group_id = serializers.IntegerField(label='商品频道组id')
    category_id = serializers.IntegerField(label='商品的一级分类id')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')

    def validate_category_id(self, value):
        # 一级分类是否存在
        try:
            GoodsCategory.objects.get(id=value, parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类ID不正确')
        return value

    def validate_group_id(self, value):
        # 频道组是否存在
        try:
            GoodsChannelGroup.objects.get(id=value)

        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')
        return value


# 频道组
class ChannelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


# 一级类别
class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')
