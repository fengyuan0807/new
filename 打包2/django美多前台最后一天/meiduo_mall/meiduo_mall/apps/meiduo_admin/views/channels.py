from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelGroupSerializer, GoodsCategorySerializer
from rest_framework.generics import ListAPIView


# 获取频道表数据 list,create,update,destory,retrieve
class ChannelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = GoodsChannel.objects.all()
    lookup_value_regex = '\d+'
    serializer_class = ChannelSerializer

    # 获取所有 get-->list
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer=self.get_serializer(queryset,many=True)
    #     return Response(serializer.data)
    # 新增 post-->create
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception = True) # 需要想一下要不要自定义验证方法
    #     serializer.save()#需要想一下用update或者是create方法，再想一下要不要自定义create和update方法
    #     return Response(serializer.data,201)
    # 获取指定 get-->retrieve
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # 修改 put-->update
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    # 删除 delete-->destory 物理删除
    # def destroy(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     instance.delete()
    #     return Response(status=204)

    # def destroy(self, request, *args, **kwargs):  # 逻辑删除
    #     instance = self.get_object()
    #     instance.is_deleted =True
    #     instance.save()
    #     return Response(statu=204)


# 新增频道表数据
# 1、获取所有的频道组
class ChannelGroupView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = ChannelGroupSerializer
    pagination_class = None


# 2. 获取一级分类数据
class GoodsCategoryView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.filter(parent=None)
    serializer_class = GoodsCategorySerializer
    pagination_class = None

# 获取三级分类
class GoodCategory3View(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.filter(subs=None)
    serializer_class = GoodsCategorySerializer
    pagination_class = None