# 手机号重复注册

### 1. 手机号重复注册逻辑分析

<img src="/user-register/images/15手机号重复注册逻辑分析.png" style="zoom:50%">

### 2. 手机号重复注册接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /mobiles/(?P&lt;mobile&gt;1[3-9]\d{9})/count/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **mobile** | string | 是 | 手机号 |

> **3.响应结果：JSON**

| 响应结果 | 响应内容 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **count** | 记录该用户名的个数 |

### 3. 手机号重复注册后端逻辑

```python
class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})
```

### 4. 手机号重复注册前端逻辑

```js
if (this.error_mobile == false) {
    let url = '/mobiles/'+ this.mobile + '/count/';
    axios.get(url, {
        responseType: 'json'
    })
        .then(response => {
            if (response.data.count == 1) {
                this.error_mobile_message = '手机号已存在';
                this.error_mobile = true;
            } else {
                this.error_mobile = false;
            }
        })
        .catch(error => {
            console.log(error.response);
        })
}
```