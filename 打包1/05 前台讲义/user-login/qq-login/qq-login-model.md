# 定义QQ登录模型类

> QQ登录成功后，我们需要将QQ用户和美多商场用户关联到一起，方便下次QQ登录时使用，所以我们选择使用MySQL数据库进行存储。

### 1. 定义模型类基类

> 为了给项目中模型类补充数据**`创建时间`**和**`更新时间`**两个字段，我们需要定义模型类基类。
> 在`meiduo_mall.utils/models.py`文件中创建模型类基类。
    
```python
from django.db import models

class BaseModel(models.Model):
    """为模型类补充字段"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
```

### 2. 定义QQ登录模型类

> 创建一个新的应用`oauth`，用来实现QQ第三方认证登录。

```python
# oauth
url(r'^oauth/', include('oauth.urls')),
```

> 在`oauth/models.py`中定义QQ身份（openid）与用户模型类User的关联关系

```python
from django.db import models

from meiduo_mall.utils.models import BaseModel
# Create your models here.s


class OAuthQQUser(BaseModel):
    """QQ登录用户数据"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.C harField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name
```

### 3. 迁移QQ登录模型类

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<img src="/user-login/images/09QQ登录表存储效果.png" style="zoom:50%">

