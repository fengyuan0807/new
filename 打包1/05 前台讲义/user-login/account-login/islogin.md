# 判断用户是否登录

### 1. 展示用户中心界面

```python
class UserInfoView(View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')
```

> 需求：
* 当用户登录后，才能访问用户中心。
* 如果用户未登录，就不允许访问用户中心，将用户引导到登录界面。

> 实现方案：
* 需要判断用户是否登录。
* 根据是否登录的结果，决定用户是否可以访问用户中心。

### 2. `is_authenticate` 判断用户是否登录

> 介绍：
* Django用户认证系统提供了方法`request.user.is_authenticated()`来判断用户是否登录。
* 如果通过登录验证则返回**True**。反之，返回**False**。
* 缺点：登录验证逻辑很多地方都需要，所以该代码需要重复编码好多次。

```python
class UserInfoView(View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        if request.user.is_authenticated():
            return render(request, 'user_center_info.html')
        else:
            return redirect(reverse('users:login'))
```

### 3. `login_required装饰器` 判断用户是否登录

* Django用户认证系统提供了装饰器`login_required`来判断用户是否登录。
    * 内部封装了`is_authenticate`
    * 位置：`django.contrib.auth.decorators`
* 如果通过登录验证则进入到视图内部，执行视图逻辑。
* 如果未通过登录验证则被重定向到`LOGIN_URL`配置项指定的地址。
    * 如下配置：表示当用户未通过登录验证时，将用户重定向到登录页面。
    ```python
    LOGIN_URL = '/login/'
    ```

> **1.装饰`as_view()`方法返回值**

> 提示：
* `login_required装饰器`可以直接装饰函数视图，但是本项目使用的是类视图。
* `as_view()`方法的返回值就是将类视图转成的函数视图。

> 结论：
* 要想使用`login_required装饰器`装饰类视图，可以间接的装饰`as_view()`方法的返回值，以达到预期效果。

```python
url(r'^info/$', login_required(views.UserInfoView.as_view()), name='info'),
```

```python
class UserInfoView(View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')
```

> **2.定义View子类封装`login_required装饰器`**
* 提示：`LoginRequired(object)`依赖于视图类`View`，复用性很差。

```python
url(r'^info/$', views.UserInfoView.as_view(), name='info'),
```

```python
class LoginRequired(View):
  """验证用户是否登陆"""

  @classmethod
  def as_view(cls, **initkwargs):
      # 自定义as_view()方法中，调用父类的as_view()方法
      view = super().as_view()
      return login_required(view)


class UserInfoView(LoginRequired):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')
```

> **3.定义obejct子类封装`login_required装饰器`**
* 提示：`LoginRequired(object)`不依赖于任何视图类，复用性更强。

```python
url(r'^info/$', views.UserInfoView.as_view(), name='info'),
```

```python
class LoginRequired(object):
  """验证用户是否登陆"""

  @classmethod
  def as_view(cls, **initkwargs):
      # 自定义as_view()方法中，调用父类的as_view()方法
      view = super().as_view()
      return login_required(view)


class UserInfoView(LoginRequired, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')
```

> **4.定义验证用户是否登录扩展类**
* 提示：定义扩展类方便项目中导入和使用(`meiduo_mall.utils.views.py`)

```python
class LoginRequiredMixin(object):
  """验证用户是否登录扩展类"""

  @classmethod
  def as_view(cls, **initkwargs):
      # 自定义的as_view()方法中，调用父类的as_view()方法
      view = super().as_view()
      return login_required(view)
 ```
 
 ```python
 class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')
 ```

### 4. 登录时next参数的使用

> **1.next参数的效果**

```
http://127.0.0.1:8000/login/?next=/info/
```

<img src="/user-login/images/05next.gif" style="zoom:50%">

> **2.next参数的作用**
* 由Django用户认证系统提供，搭配`login_required装饰器`使用。
* 记录了用户未登录时访问的地址信息，可以帮助我们实现在用户登录成功后直接进入未登录时访问的地址。

```python
# 响应登录结果
next = request.GET.get('next')
if next:
    response = redirect(next)
else:
    response = redirect(reverse('contents:index'))
```

<img src="/user-login/images/06next_redirect.gif" style="zoom:50%">

### 5. 知识要点

1. 判断用户是否登录依然使用状态保持信息实现。
2. 项目中很多接口都是需要用户登录才能访问的，所以为了方便编码，我们将判断用户登录的操作封装到装饰器中。
3. 登录时next参数的作用是为了方便用户从哪里进入到登录页面，登录成功后就回到哪里。

