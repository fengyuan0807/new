from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from goods.models import SPU, SPUSpecification

from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer


# 获取SPU简单数据 get
class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer
    pagination_class = None


# 获取SPU商品规格信息
class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs['pk']
        spu_specs = SPUSpecification.objects.filter(spu_id=pk)
        return spu_specs

    serializer_class = SPUSpecSerializer
    pagination_class = None
    # 获取所有SPU的规格 　get
    # def get(self, request, pk):　# APIView
    #     spu_specs = SPUSpecification.objects.filter(spu_id=pk)
    #     serializer=self.get_serializer(spu_specs,many=True)
    #     return Response(serializer.data)
