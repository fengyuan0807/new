# 追加导包路径

> 思考：
* 是否可以将注册users应用做的更加简便？
* 按照如下形式，直接以应用名users注册

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users', # 用户模块应用
]
```

> 分析：
* 已知导包路径
    * `meiduo_project/meiduo_mall`
* 已知'users'应用所在目录
    * `meiduo_project/meiduo_mall/meiduo_mall/apps/users`
* 若要直接以应用名'users'注册
    * 需要一个导包路径：`meiduo_project/meiduo_mall/meiduo_mall/apps`

> **解决办法**
    * 追加导包路径：`meiduo_project/meiduo_mall/meiduo_mall/apps`

### 1. 追加导包路径

> **1.查看项目BASE_DIR**

<img src="/user-register/images/04查看项目BASE_DIR.png" style="zoom:50%">

> **2.追加导包路径**

<img src="/user-register/images/03查看项目导包路径.png" style="zoom:90%">

<img src="/user-register/images/05追加导包路径.png" style="zoom:90%">

### 2. 重新注册用户模块应用

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users', # 用户模块应用
]
```

> 重新注册完users应用后，运行测试程序。

### 3. 知识要点

1. 查看导包路径
    * 通过查看导包路径，可以快速的知道项目中各个包该如何的导入。
    * 特别是接手老项目时，可以尽快的适应项目导包的方式。
2. 追加导包路径
    * 通过追加导包路径，可以简化某些目录复杂的导包方式。
