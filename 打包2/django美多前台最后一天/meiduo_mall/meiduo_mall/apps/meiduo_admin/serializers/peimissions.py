import re

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.models import User


# 权限系列化器
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


# 权限类型序列化器
class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id', 'name')


# 用户组序列化器
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


# 权限简单序列化器
class PermissionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')


# 管理员用户序列化器
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'groups', 'user_permissions', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True
            }
        }

    def validate_mobile(self, value):
        if not re.match('^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError('手机号已经存在')
        return value

    def create(self, validated_data):
        validated_data['is_staff'] = True

        # validated_data.pop('groups')
        # validated_data.pop('user_permissions')
        # password = validated_data.get('password')
        # if not password:
        #     password = '123456abc'
        #     validated_data['password'] = password
        # user = User.objects.create_user(**validated_data)
        # return user

        user = super().create(validated_data)
        password = validated_data.get('password')
        if not password:
            password = '123456abc'
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """修改管理员用户"""
        # 从`validated_data`中去除密码`password`
        password = validated_data.pop('password', None)

        # 修改管理员账户信息
        super().update(instance, validated_data)

        # 修改密码
        if password:
            instance.set_password(password)
            instance.save()

        return instance


# 管理员用户组简单序列化器
class GroupSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
