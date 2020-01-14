# 用户注册后端逻辑

### 1. 接收参数

> 提示：用户注册数据是从注册表单发送过来的，所以使用**`request.POST`**来提取。

```python
username = request.POST.get('username')
password = request.POST.get('password')
password2 = request.POST.get('password2')
mobile = request.POST.get('mobile')
allow = request.POST.get('allow')
```

### 2. 校验参数
> 前端校验过的后端也要校验，后端的校验和前端的校验是一致的

```
# 判断参数是否齐全
# 判断用户名是否是5-20个字符
# 判断密码是否是8-20个数字
# 判断两次密码是否一致
# 判断手机号是否合法
# 判断是否勾选用户协议
```

```python
# 判断参数是否齐全
if not all([username, password, password2, mobile, allow]):
    return http.HttpResponseForbidden('缺少必传参数')
# 判断用户名是否是5-20个字符
if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
    return http.HttpResponseForbidden('请输入5-20个字符的用户名')
# 判断密码是否是8-20个数字
if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
    return http.HttpResponseForbidden('请输入8-20位的密码')
# 判断两次密码是否一致
if password != password2:
    return http.HttpResponseForbidden('两次输入的密码不一致')
# 判断手机号是否合法
if not re.match(r'^1[3-9]\d{9}$', mobile):
    return http.HttpResponseForbidden('请输入正确的手机号码')
# 判断是否勾选用户协议
if allow != 'on':
    return http.HttpResponseForbidden('请勾选用户协议')
```

> 提示：这里校验的参数，前端已经校验过，如果此时参数还是出错，说明该请求是非正常渠道发送的，所以直接禁止本次请求。

### 3. 保存注册数据
> * 这里使用Django认证系统用户模型类提供的 **create_user()** 方法创建新的用户。
> * 这里 **create_user()** 方法中封装了 **set_password()** 方法加密密码。

```python
# 保存注册数据
try:
    User.objects.create_user(username=username, password=password, mobile=mobile)
except DatabaseError:
    return render(request, 'register.html', {'register_errmsg': '注册失败'})

# 响应注册结果
return http.HttpResponse('注册成功，重定向到首页')
```

> 如果注册失败，我们需要在页面上渲染出注册失败的提示信息。

```html
{% if register_errmsg %}
    <span class="error_tip2">{{ register_errmsg }}</span>
{% endif %}
```

### 4. 响应注册结果

* **重要提示：注册成功，重定向到首页**

> **1.创建首页广告应用：contents**

```bash
$ cd ~/projects/meiduo_project/meiduo_mall/meiduo_mall/apps
$ python ../../manage.py startapp contents
```

<img src="/user-register/images/11广告首页应用.png" style="zoom:50%">

> **2.定义首页广告视图：IndexView**

```python
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        return render(request, 'index.html')
```

> **3.配置首页广告路由：绑定命名空间**

```python
# contents
url(r'^', include('contents.urls', namespace='contents')),
```
```python
# 首页广告
url(r'^$', views.IndexView.as_view(), name='index'),
```

> **4.测试首页广告是否可以正常访问**

```
http://127.0.0.1:8000/
```

> **5.响应注册结果：重定向到首页**

```python
# 响应注册结果
return redirect(reverse('contents:index'))
```

### 5. 知识要点

1. 后端逻辑编写套路：
    * 业务逻辑分析
    * 接口设计和定义
    * 接收和校验参数
    * 实现主体业务逻辑
    * 响应结果
2. 注册业务逻辑核心思想：
    * 保存用户注册数据


