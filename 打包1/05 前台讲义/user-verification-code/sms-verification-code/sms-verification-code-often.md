# 避免频繁发送短信验证码

> 存在的问题：
* 虽然我们在前端界面做了60秒倒计时功能。
* 但是恶意用户可以绕过前端界面向后端频繁请求短信验证码。

> 解决办法：
* 在后端也要限制用户请求短信验证码的频率。60秒内只允许一次请求短信验证码。
* 在Redis数据库中缓存一个数值，有效期设置为60秒。

### 1. 避免频繁发送短信验证码逻辑分析

<img src="/user-verification-code/images/23避免频繁发送短信验证码逻辑分析.png" style="zoom:50%">

### 2. 避免频繁发送短信验证码逻辑实现

> **1.提取、校验send_flag**

```python
send_flag = redis_conn.get('send_flag_%s' % mobile)
if send_flag:
    return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})
```

> **2.重新写入send_flag**

```python
# 保存短信验证码
redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
# 重新写入send_flag
redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
```

> **3.界面渲染频繁发送短信提示信息**

```python
if (response.data.code == '4001') {
    this.error_image_code_message = response.data.errmsg;
    this.error_image_code = true;
} else { // 4002
    this.error_sms_code_message = response.data.errmsg;
    this.error_sms_code = true;
}
```

