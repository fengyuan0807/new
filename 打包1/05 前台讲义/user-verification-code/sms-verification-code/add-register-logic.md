# 补充注册时短信验证逻辑

### 1. 补充注册时短信验证后端逻辑

> **1.接收短信验证码参数**

```python
sms_code_client = request.POST.get('sms_code')
```

> **2.保存注册数据之前，对比短信验证码**

```python
redis_conn = get_redis_connection('verify_code')
sms_code_server = redis_conn.get('sms_%s' % mobile)
if sms_code_server is None:
    return render(request, 'register.html', {'sms_code_errmsg':'无效的短信验证码'})
if sms_code_client != sms_code_server.decode():
    return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
```

### 2. 补充注册时短信验证前端逻辑

> **1.register.html**

```html
<li>
    <label>短信验证码:</label>
    <input type="text" v-model="sms_code" @blur="check_sms_code" name="sms_code" id="msg_code" class="msg_input">
    <a @click="send_sms_code" class="get_msg_code">[[ sms_code_tip ]]</a>
    <span v-show="error_sms_code" class="error_tip">[[ error_sms_code_message ]]</span>
    {% if sms_code_errmsg %}
        <span class="error_tip">{{ sms_code_errmsg }} </span>
    {% endif %}
</li>
```
