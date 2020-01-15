from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption


# 获取SPU商品简单信息序列化器
class SPUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ('id', 'name')

# SPU规格选项参数序列化器类
class SpecificationOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


# 获取SPU商品规格信息序列化器
class SPUSpecSerializer(serializers.ModelSerializer):
    options = SpecificationOptionSerializer(label='规格选项参数', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'options')
