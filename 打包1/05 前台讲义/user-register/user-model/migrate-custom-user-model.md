# 迁移用户模型类

### 1. 指定用户模型类

> 思考：为什么Django默认用户模型类是User？
* 阅读源代码：'django.conf.global_settings'
```python
AUTH_USER_MODEL = 'auth.User'
```

> 结论：
* Django用户模型类是通过全局配置项 **AUTH_USER_MODEL** 决定的

> 配置规则：
```python
AUTH_USER_MODEL = '应用名.模型类名'
```

```python
# 指定本项目用户模型类
AUTH_USER_MODEL = 'users.User'
```

### 2. 迁移用户模型类

> **1.创建迁移文件**
* `python manage.py makemigrations`

<img src="/user-register/images/07创建迁移文件.png" style="zoom:50%">

> **2.执行迁移文件**
* `python manage.py migrate`
    
<img src="/user-register/images/08执行迁移文件.png" style="zoom:50%">
    
### 3. 知识要点

1. 用户认证系统中的用户模型类，是通过全局配置项 **AUTH_USER_MODEL** 决定的。
2. 如果迁移自定义用户模型类，**必须先配置 AUTH_USER_MODEL** 。






