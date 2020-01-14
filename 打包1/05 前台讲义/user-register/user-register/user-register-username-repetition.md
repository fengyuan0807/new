# 用户名重复注册

### 1. 用户名重复注册逻辑分析

<img src="/user-register/images/14用户名重复注册逻辑分析.png" style="zoom:50%">

### 2. 用户名重复注册接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /usernames/(?P&lt;username&gt;[a-zA-Z0-9_-]{5,20})/count/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **username** | string | 是 | 用户名 |

> **3.响应结果：JSON**

| 响应结果 | 响应内容 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **count** | 记录该用户名的个数 |

### 3. 用户名重复注册后端逻辑

```python
class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
```

### 4. 用户名重复注册前端逻辑

```js
if (this.error_name == false) {
    let url = '/usernames/' + this.username + '/count/';
    axios.get(url,{
        responseType: 'json'
    })
        .then(response => {
            if (response.data.count == 1) {
                this.error_name_message = '用户名已存在';
                this.error_name = true;
            } else {
                this.error_name = false;
            }
        })
        .catch(error => {
            console.log(error.response);
        })
}
```

### 5. 知识要点

1. 判断用户名重复注册的核心思想：
    * 使用用户名查询该用户名对应的记录是否存在，如果存在，表示重复注册了，反之，没有重复注册。
2. axios发送异步请求套路：
    * 处理用户交互
    * 收集请求参数
    * 准备请求地址
    * 发送异步请求
    * 得到服务器响应
    * 控制界面展示效果








