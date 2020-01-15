from rest_framework import serializers

from goods.models import GoodsVisitCount


class GoodsVisitCountSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(label='名称')

    class Meta:
        model = GoodsVisitCount
        fields = ('count', 'category')
        extra_kwargs = {
            'count': {'min_value': '0'}
        }
