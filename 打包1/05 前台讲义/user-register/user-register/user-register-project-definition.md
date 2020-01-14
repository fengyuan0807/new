# 用户注册接口设计和定义

### 1. 设计接口基本思路

* 对于接口的设计，我们要根据具体的业务逻辑，设计出适合业务逻辑的接口。
* 设计接口的思路：
    * 分析要实现的业务逻辑：
        * 明确在这个业务中涉及到几个相关子业务。
        * 将每个子业务当做一个接口来设计。
    * 分析接口的功能任务，明确接口的访问方式与返回数据：
        * 请求方法（如GET、POST、PUT、DELETE等）。
        * 请求地址。
        * 请求参数（如路径参数、查询字符串、表单、JSON等）。
        * 响应数据（如HTML、JSON等）。

### 2. 用户注册接口设计

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /register/ |

> **2.请求参数：表单参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **username** | string | 是 | 用户名 |
| **password** | string | 是 | 密码 |
| **password2** | string | 是 | 确认密码 |
| **mobile** | string | 是 | 手机号 |
| **sms_code** | string | 是 | 短信验证码 |
| **allow** | string | 是 | 是否同意用户协议 |

> **3.响应结果：HTML**
* `register.html`

| 响应结果 | 响应内容 |
| ---------------- | ---------------- |
| **注册失败** | 响应错误提示 |
| **注册成功** | 重定向到首页 |

### 3. 用户注册接口定义

> **1.注册视图**

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

    def post(self, request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """
        pass
```

> **2.总路由**

```python
urlpatterns = [
    # users
    url(r'^', include('users.urls', namespace='users')),
]
```

> **3.子路由**

```python
urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
```