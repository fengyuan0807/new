# 定义用户模型类

### 1. Django默认用户认证系统

* Django自带用户认证系统
    * 它处理用户账号、组、权限以及基于cookie的用户会话。
* Django认证系统位置
    * `django.contrib.auth`包含认证框架的核心和默认的模型。
    * `django.contrib.contenttypes`是Django内容类型系统，它允许权限与你创建的模型关联。
* Django认证系统同时处理认证和授权
    * 认证：验证一个用户是否它声称的那个人，可用于账号登录。
    * 授权：授权决定一个通过了认证的用户被允许做什么。
* Django认证系统包含的内容
    * 用户：**用户模型类**、用户认证。
    * 权限：标识一个用户是否可以做一个特定的任务，MIS系统常用到。
    * 组：对多个具有相同权限的用户进行统一管理，MIS系统常用到。
    * 密码：一个可配置的密码哈希系统，设置密码、密码校验。

### 2. Django默认用户模型类

* Django认证系统中提供了用户模型类User保存用户的数据。
    * **User对象是认证系统的核心。**
* Django认证系统用户模型类位置
    * **django.contrib.auth.models.User**

    <img src="/user-register/images/06Django默认用户模型类.png" style="zoom:50%">

* 父类**AbstractUser**介绍
    * User对象基本属性
        * 创建用户(注册用户)必选： `username、password`
        * 创建用户(注册用户)可选：`email、first_name、last_name、last_login、date_joined、is_active 、is_staff、is_superuse`
        * 判断用户是否通过认证(是否登录)：`is_authenticated`
    * 创建用户(注册用户)的方法
    ```python
    user = User.objects.create_user(username, email, password, **extra_fields)
    ```
    * 用户认证(用户登录)的方法
    ```python
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password, **kwargs)
    ```
    * 处理密码的方法
        * 设置密码：`set_password(raw_password)`
        * 校验密码：`check_password(raw_password)`

### 3. 自定义用户模型类

> 思考：为什么要自定义用户模型类？
* 观察注册界面会发现，美多商城`注册数据`中`必选用户mobile信息`。
* 但是Django默认用户模型类中没有mobile字段，所以要自定义用户模型类。

> 如何自定义用户模型类？
* 继承自**AbstractUser**（可通过阅读Django默认用户模型类的源码得知） 。
* 新增`mobile`字段。

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
```

### 4. 知识要点

1. Django自带**用户认证系统**，**核心就是User对象**，并封装了一系列可用的方法和属性。
2. Django用户认证系统包含了一系列对用户的操作，比如：模型类，认证，权限，分组，密码处理等。
3. Django用户认证系统中的用户模型类可以自定义，继承自**AbstractUser**。
4. [Django用户认证系统说明文档](https://yiyibooks.cn/xx/Django_1.11.6/topics/auth/index.html)

