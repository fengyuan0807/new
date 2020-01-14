# 创建用户模块子应用

### 1. 创建用户模块子应用

> **1.准备`apps`包，用于管理所有应用**
    
<img src="/user-register/images/01准备应用包.png" style="zoom:50%">

> **2.在`apps`包下创建应用`users`**

```bash
$ cd ~/projects/meiduo_project/meiduo_mall/meiduo_mall/apps
$ python ../../manage.py startapp users
```

<img src="/user-register/images/02创建users应用.png" style="zoom:50%">

### 2. 查看项目导包路径

> 重要提示：
* 若要知道如何导入users应用并完成注册，需要知道**项目导包路径**

<img src="/user-register/images/03查看项目导包路径.png" style="zoom:50%">

> 已知导包路径
* `meiduo_project/meiduo_mall`

> 已知 'users'应用所在目录
* `meiduo_project/meiduo_mall/meiduo_mall/apps/users`

> 得到导入'users'应用的导包路径是：`meiduo_mall/apps/users`

### 3. 注册用户模块子应用

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'meiduo_mall.apps.users', # 用户模块应用
]
```

> 注册完users应用后，运行测试程序。
