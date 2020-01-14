# 短信验证码后端逻辑

### 1. 短信验证码接口设计

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /sms_codes/(?P&lt;mobile&gt;1[3-9]\d{9})/ |

> **2.请求参数：路径参数和查询字符串**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **mobile** | string | 是 | 手机号 |
| **image_code** | string | 是 | 图形验证码 |
| **uuid** | string | 是 | 唯一编号 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

### 2. 短信验证码接口定义

```python
class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        pass
```

### 3. 短信验证码后端逻辑实现

```python
class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        # 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)
        # 保存短信验证码
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 发送短信验证码
        CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
```
