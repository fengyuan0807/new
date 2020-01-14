# 多账号登录

> * Django自带的用户认证后端默认是使用用户名实现用户认证的。

> * 用户认证后端位置：django.contrib.auth.backends.ModelBackend。

> * 如果想实现用户名和手机号都可以认证用户，就需要自定义用户认证后端。

> * 自定义用户认证后端步骤
    * 在users应用中新建utils.py文件
    * 新建类，继承自ModelBackend
    * 重写认证authenticate()方法
    * 分别使用用户名和手机号查询用户
    * 返回查询到的用户实例

### 1. 自定义用户认证后端

> users.utils.py

```python
from django.contrib.auth.backends import ModelBackend
import re
from .models import User


def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名或者手机号
    :return: user
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现多账号登录
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """
        # 根据传入的username获取user对象。username可以是手机号也可以是账号
        user = get_user_by_account(username)
        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user
```

### 2. 配置自定义用户认证后端

> **1.Django自带认证后端源码**

<img src="/user-login/images/02Django自带认证后端源码.png" style="zoom:50%">

> **2.配置自定义用户认证后端**

```python
# 指定自定义的用户认证后端
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']
```

### 3. 测试自定义用户认证后端

<img src="/user-login/images/03测试自定义认证后端.png" style="zoom:50%">

### 4. 知识要点

1. Django自带的用户认证系统只会使用用户名去认证一个用户。
    * 所以我们为了实现多账号登录，就可以自定义认证后端，采用其他的唯一信息去认证一个用户。

