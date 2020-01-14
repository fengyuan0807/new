# 验证邮箱后端逻辑

### 1. 验证邮箱接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /emails/verification/ |

> **2.请求参数：查询参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **token** | string | 是 | 邮箱激活链接 |

> **3.响应结果：HTML**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **邮箱验证失败** | 响应错误提示 |
| **邮箱验证成功** | 重定向到用户中心 |

### 2. 验证链接提取用户信息

```python
def check_verify_email_token(token):
    """
    验证token并提取user
    :param token: 用户信息签名后的结果
    :return: user, None
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user
```

### 3. 验证邮箱后端逻辑实现

> 验证邮箱的核心：就是将用户的`email_active`字段设置为`True`

```python
class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        """实现邮箱验证逻辑"""
        # 接收参数
        token = request.GET.get('token')

        # 校验参数：判断token是否为空和过期，提取user
        if not token:
            return http.HttpResponseBadRequest('缺少token')

        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')

        # 修改email_active的值为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 返回邮箱验证结果
        return redirect(reverse('users:info'))
```