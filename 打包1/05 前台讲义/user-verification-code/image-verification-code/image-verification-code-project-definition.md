# 图形验证码接口设计和定义

### 1. 图形验证码接口设计

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | image_codes/(?P&lt;uuid&gt;[\w-]+)/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **uuid** | string | 是 | 唯一编号 |

> **3.响应结果：`image/jpg`**

<img src="/user-verification-code/images/02图形验证码1.png" style="zoom:50%">

### 2. 图形验证码接口定义

> **1.图形验证码视图**

```python
class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        pass
```

> **2.总路由**

```python
# verifications
url(r'^', include('verifications.urls')),
```

> **3.子路由**

```python
# 图形验证码
url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
```
