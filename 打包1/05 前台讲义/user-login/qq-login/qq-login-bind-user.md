# openid是否绑定用户的处理

<img src="/user-login/images/11openid绑定用户.png" style="zoom:50%">

### 1. 判断openid是否绑定过用户

> 使用openid查询该QQ用户是否在美多商城中绑定过用户。

```python
try:
    oauth_user = OAuthQQUser.objects.get(openid=openid)
except OAuthQQUser.DoesNotExist:
    # 如果openid没绑定美多商城用户
    pass
else:
    # 如果openid已绑定美多商城用户
    pass
```

### 2. openid已绑定用户的处理

> 如果openid已绑定美多商城用户，直接生成状态保持信息，登录成功，并重定向到首页。

```python
try:
    oauth_user = OAuthQQUser.objects.get(openid=openid)
except OAuthQQUser.DoesNotExist:
    # 如果openid没绑定美多商城用户
    pass
else:
    # 如果openid已绑定美多商城用户
    # 实现状态保持
    qq_user = oauth_user.user
    login(request, qq_user)

    # 响应结果
    next = request.GET.get('state')
    response = redirect(next)

    # 登录时用户名写入到cookie，有效期15天
    response.set_cookie('username', qq_user.username, max_age=3600 * 24 * 15)

    return response
```

### 3. openid未绑定用户的处理

> * 为了能够在后续的绑定用户操作中前端可以使用openid，在这里将openid签名后响应给前端。
> * openid属于用户的隐私信息，所以需要将openid签名处理，避免暴露。

```python
try:
    oauth_user = OAuthQQUser.objects.get(openid=openid)
except OAuthQQUser.DoesNotExist:
    # 如果openid没绑定美多商城用户
    access_token = generate_eccess_token(openid)
    context = {'access_token': access_token}
    return render(request, 'oauth_callback.html', context)
else:
    # 如果openid已绑定美多商城用户
    # 实现状态保持
    qq_user = oauth_user.user
    login(request, qq_user)

    # 重定向到主页
    response = redirect(reverse('contents:index'))

    # 登录时用户名写入到cookie，有效期15天
    response.set_cookie('username', qq_user.username, max_age=3600 * 24 * 15)

    return response
```

> `oauth_callback.html`中渲染`access_token`

```python
<input v-model="access_token" type="hidden" name="access_token" value="{{ access_token }}">
```

### 4. 补充itsdangerous的使用
> * `itsdangerous`模块的参考资料链接 http://itsdangerous.readthedocs.io/en/latest/

> * 安装：`pip install itsdangerous`

> * `TimedJSONWebSignatureSerializer`的使用
    * 使用`TimedJSONWebSignatureSerializer`可以**生成带有有效期**的`token`

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

# serializer = Serializer(秘钥, 有效期秒)
serializer = Serializer(settings.SECRET_KEY, 300)
# serializer.dumps(数据), 返回bytes类型
token = serializer.dumps({'mobile': '18512345678'})
token = token.decode()

# 检验token
# 验证失败，会抛出itsdangerous.BadData异常
serializer = Serializer(settings.SECRET_KEY, 300)
try:
    data = serializer.loads(token)
except BadData:
    return None
```

> **补充：openid签名处理**
* `oauth.utils.py`

```python
def generate_eccess_token(openid):
    """
    签名openid
    :param openid: 用户的openid
    :return: access_token
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()
```



