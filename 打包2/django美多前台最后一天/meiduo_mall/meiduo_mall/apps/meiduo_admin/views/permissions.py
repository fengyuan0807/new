from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.peimissions import PermissionSerializer, ContentTypeSerializer, GroupSerializer, \
    PermissionSimpleSerializer, AdminUserSerializer, GroupSimpleSerializer
from users.models import User

# 获取权限列表数据
class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    lookup_value_regex = '\d'

    # 获取所有的权限列表数据 get-->list
    # GET/meiduo_admin/permission/perms/
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset,many=True)
    #     return Response(serializer.data)
    # 新建权限列表数据 post-->create
    # POST/meiduo_admin/permission/perms/
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid()
    #     serializer.save()
    #     return Response(serializer.data, status=201)
    # 获取制定权限列表数据
    # GET /meiduo_admin/permission/perms/(?P<pk>\d+)
    # def retrieve(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     serializer=self.get_serializer(instance)
    #     return Response(serializer.data)
    # 修改制定权限列表数据
    # PUT /meiduo_admin/permission/perms/(?P<pk>\d+) -->update
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer=self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    # 删除制定权限列表数据
    # destory/meiduo_admin/permission/perms/(?P<pk>\d+)
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.deletc()
    #     return Response(status=204)

    # 获取权限类型 content_type
    # GET /meiduo_admin/permission/content_types/
    # def content_types(self, request):
    #     contenttypes = ContentType.objects.all()
    #     serializer = ContentTypeSerializer(contenttypes, many=True)
    #     return Response(serializer.data)


# 获取权限类型
class Content_typesView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    pagination_class = None

    # def list(self, request, *args, **kwargs):
    #     queryset=ContentType.objects.all()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


# 获取用户组表列表数据
class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # 获取所有用户组数据
    # GET/meiduo_admin/permission/groups/
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    # 新增用户组数据 POST /meiduo_admin/permission/groups/
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(date=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=201)
    # 获取指定用户组数据 GET /meiduo_admin/permission/groups/(?P<pk>\d+) -->retrieve
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    # # 更新指定用户组数据 PUT /meiduo_admin/permission/groups/(?P<pk>\d+)--> update
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer =self.get_serializer(instance,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return  Response(204)

# 获取权限简单数据 GET/meiduo_admin/permission/simple/ -->simple
    def simple(self, request, *args, **kwargs):
        queryset = Permission.objects.all()
        serializer = PermissionSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

# 获取管理员用户列表数据
class AdminUserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer
    # queryset = User.objects.filter(is_staff=True)
    def get_queryset(self):
        users = User.objects.filter(is_staff=True)
        return users

    # 获取所有 GET /meiduo_admin/permission/admins/ -->list
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    # 新增管理员用户POST /meiduo_admin/permission/admins/ -->create
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 获取制定管理员
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    # 修改
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
# 获取简单用户组简单数据GET/meiduo_admin/permission/groups/simple/ -->simple

    def simple(self,request,*args,**kwargs):
        groups = Group.objects.all()
        serializer = GroupSimpleSerializer(groups,many=True)
        return Response(serializer.data)