# 展示用户注册页面

### 1. 准备用户注册模板文件

<img src="/user-register/images/10准备注册模板文件.png" style="zoom:50%">

> 加载页面静态文件

```html
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>美多商城-注册</title>
    <link rel="stylesheet" type="text/css" href="{{ static('css/reset.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ static('css/main.css') }}">
</head>
```

### 2. 定义用户注册视图

```python
class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')
```

### 3. 定义用户注册路由

> **1.总路由**

```python
urlpatterns = [
    # users
    url(r'^', include('users.urls', namespace='users')),
]
```

> **2.子路由**

```python
urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
```