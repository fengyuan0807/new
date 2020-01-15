from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage, SKU, SPU
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer
from django.db.models import Q


# 获取图片表数据
class SKUImagesViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer

    # 查找所有的 get-->list
    # def list(self, request, *args, **kwargs):
    #     queryset=self.get_queryset()
    #     serializer = self.get_serializer(queryset,many=True)
    #     return Response(serializer.data)
    # 新增图片 post-->create
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid() 是否需要重写
    #     serializer.save()是否需要重写
    #     return Response(serializer.data, status=201)
    # 获取指定的 get-->retrieve
    # def retrieve(self, request, *args, **kwargs):
    #     sku_image = self.get_object()
    #     serializer = self.get_serializer(sku_image)
    #     return Response(serializer.data)
    # 修改图片 put-->update
    # def update(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     serializer=self.get_serializer(instance,data=request.data)
    #     serializer.is_valid()
    #     serializer.save()
    #     return Response(serializer.data)
    # 删除图片 delete-->destory
    # def destroy(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     instance.delete()
    #     return Response(204)
# 获取SKU商品简单数据
class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer
    pagination_class = None

# 获取SKU表数据
class SKUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SKUSerializer
    # queryset=None
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        else:
            skus = SKU.objects.all()
        return skus

    # 获取所有的 sku get-->list
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    #新增sku post-->create
    # def create(self, request, *args, **kwargs):
    #     serializer =self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #       serializer.save()
    #     return Response(serializer.data, status=201)
    # 获取指定 get retrieve
    # def retrieve(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     serializer=self.get_serializer(instance)
    #     return  Response(serializer.data)
    # 修改 sku put
    # def put(self,request,pk):
    #     instance=self.get_object()
    #     serializer = self.get_serializer(instance,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

