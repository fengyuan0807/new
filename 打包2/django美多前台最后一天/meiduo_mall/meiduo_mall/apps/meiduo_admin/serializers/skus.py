from django.db import transaction
from rest_framework import serializers
from goods.models import SKUImage, SKU, SKUSpecification, SPU, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    """SKU图片序列化器类"""
    sku_id = serializers.IntegerField(label="sku商品ID")
    sku = serializers.StringRelatedField(label='sku商品名称')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value

    def create(self, validated_data):
        sku_image = super().create(validated_data)
        sku = sku_image.sku
        # sku = SKU.objects.get(id=validated_data['sku_id'])
        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()
        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""

    class Meta:
        model = SKU
        fields = ('id', 'name')


# SKU具体规格序列化器
class SKUSpecSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='规格选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


# SKU商品序列化器类
class SKUSerializer(serializers.ModelSerializer):
    #     {
    #         "spu_id": "商品SPU ID",
    #         "specs": [
    #             {
    #                 "spec_id": "规格id",
    #                 "option_id": "选项id"
    #             },
    #             ...
    #         ]
    #       }

    spu_id = serializers.IntegerField(label='SPU ID')
    category = serializers.StringRelatedField(label='商品三级分类名称')
    # 关联对象嵌套序列化
    specs = SKUSpecSerializer(label='商品规格名称', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'comments', 'default_image', 'spu')
        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):

        # 校验　规格是否正确 是不是spu的
        # 校验　value是否正确　是不是那个规格的

        # 1.校验　spu_id 是否正确
        spu_id = attrs['spu_id']
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SKU_ID 不正确')
        # 2.校验　规格是不是spu的
        # 2.1 spu的数量
        specs = attrs['specs']  # 客户端传入的
        spu_specs = spu.specs.all()  # 数据库的
        spu_specs_count = spu_specs.count()
        if len(specs) != spu_specs_count:
            raise serializers.ValidationError('规格数据有误')
        # 2.2 spu的数据
        spec_ids = [spec.get('spec_id') for spec in specs]  # 客户端传入的spec_id
        spu_spec_ids = [spu_spec.id for spu_spec in spu_specs]  # 数据库的
        # 排序
        spec_ids.sort()
        spu_spec_ids.sort()
        if spec_ids != spu_spec_ids:
            raise serializers.ValidationError('规格数据有误')
        # 3.value是否正确　是不是那个规格的
        for spec in specs:
            spec_id = spec.get('spec_id')  # 客户端获取的
            option_id = spec.get('option_id')  # 客户端获取的
            spec_options = SpecificationOption.objects.filter(spec_id=spec_id)
            option_ids = [spec_option.id for spec_option in spec_options]
            if option_id not in option_ids:
                raise serializers.ValidationError('选项参数有错')
        # attrs中添加第三级分类ID 因为响应的有categroy
        attrs['category_id'] = spu.category3_id
        return attrs

    def create(self, validated_data):
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # sku=SKU.objects.create(**validated_data)
            sku = super().create(validated_data)
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )
        return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            sku = super().update(instance, validated_data)
            instance.specs.all().delete()
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )
        return instance