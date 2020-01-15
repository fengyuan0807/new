import re

from django.utils import timezone
from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        # 校验用户名和密码是否正确
        try:
            user = User.objects.get(username=username, is_staff=True)  # 是否是管理员
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或者密码错误')
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或者密码错误')
            attrs['user'] = user
        return attrs

    # 需要返回token，所以要重写
    def create(self, validated_data):
        user = validated_data['user']
        # 更新管理员的登陆时间
        now_time = timezone.now()
        user.last_login = now_time
        user.save()

        # 服务器生成jwt token, 保存当前用户的身份信息
        from rest_framework_jwt.settings import api_settings
        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)
        # 动态的加属性
        user.token = token
        return user


# 用户查询 新增
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')
        extra_fields = {
            'password': {
                'write_only': True,
                'mini_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度是8',
                    'max_length': '密码最大长度是20'
                }
            }
        }

    def validate_mobile(self, value):

        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式不正确')

        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError('手机号码重复')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
