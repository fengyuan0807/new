from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer
from users.models import User


# 管理员登陆
class AdminAuthorizeView(CreateAPIView):
    # class AdminAuthorizeView(CreateModelMixin,
    #                          GenericAPIView):

    serializer_class = AdminAuthSerializer

    # def post(self, request):
    #     return self.create(request)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
# class UserInfoView(GenericAPIView):
# class UserInfoView(ListModelMixin, GenericAPIView):

class UserInfoView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    # 查询用户
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            users = User.objects.filter(username__contains=keyword, is_staff=False)
        else:
            users = User.objects.filter(is_staff=False)
        return users
        # def get(self,request):
        #     return self.list(request)
        # def get(self, request):
        #     users = self.get_queryset()
        #     serializer = self.get_serializer(users, many=True)
        #     return Response(serializer.data)

        # 新增用户 GenericAPIView,CreateModelMixin
        # def post(self):
        #     return self.create(request)

        # APIView
        # def post(self, request):
        #     # 1、获取 2、校验 3、新增保存
        #     serializer = self.get_serializer(data=request.data)
        #     serializer.is_valid(raise_exception=False)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)

