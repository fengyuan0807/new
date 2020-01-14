# 添加邮箱后端逻辑

### 1. 添加邮箱接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /emails/ |

> **2.请求参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **email** | string | 是 | 邮箱 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

### 2. 添加邮箱后端逻辑实现

```python
class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return http.HttpResponseForbidden('缺少email参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        # 赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        # 响应添加邮箱结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})
```

### 3. 判断用户是否登录并返回JSON

> 重要提示：

* 只有用户登录时才能让其绑定邮箱。
* 此时前后端交互的数据类型是JSON，所以需要判断用户是否登录并返回JSON给用户。

> 方案一：
* 使用Django用户认证系统提供的`is_authenticated()`

```python
class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 判断用户是否登录并返回JSON
        if not request.user.is_authenticated():
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
        pass
```

> 方案二：
* 自定义返回JSON的`login_required`装饰器
* 在`meiduo_mall.utils.views.py`中

```python
def login_required_json(view_func):
    """
    判断用户是否登录的装饰器，并返回json
    :param view_func: 被装饰的视图函数
    :return: json、view_func
    """
    # 恢复view_func的名字和文档
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 如果用户未登录，返回json数据
        if not request.user.is_authenticated():
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
        else:
            # 如果用户登录，进入到view_func中
            return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredJSONMixin(object):
    """验证用户是否登陆并返回json的扩展类"""
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)
```

> `LoginRequiredJSONMixin`的使用

```python
class EmailView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 判断用户是否登录并返回JSON
        pass
```
