# 用户名登录

### 1. 用户名登录逻辑分析

<img src="/user-login/images/01用户名登录逻辑分析.png" style="zoom:50%">

### 2. 用户名登录接口设计

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /login/ |

> **2.请求参数：表单**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **username** | string | 是 | 用户名 |
| **password** | string | 是 | 密码 |
| **remembered** | string | 是 | 是否记住用户 |

> **3.响应结果：HTML**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **登录失败** | 响应错误提示 |
| **登录成功** | 重定向到首页 |

### 3. 用户名登录接口定义

```python
class LoginView(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """
        pass

    def post(self, request):
        """
        实现登录逻辑
        :param request: 请求对象
        :return: 登录结果
        """
        pass
```

### 4. 用户名登录后端逻辑

```python
class LoginView(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        实现登录逻辑
        :param request: 请求对象
        :return: 登录结果
        """
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')

        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 实现状态保持
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)

        # 响应登录结果
        return redirect(reverse('contents:index'))
```

### 5. 知识要点

1. 登录的核心思想：认证和状态保持
    * 通过用户的认证，确定该登录用户是美多商场的注册用户。
    * 通过状态保持缓存用户的唯一标识信息，用于后续是否登录的判断。

