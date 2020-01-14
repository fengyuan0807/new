# 图形验证码后端逻辑

### 1. 准备captcha扩展包

> 提示：`captcha`扩展包用于后端生成图形验证码

<img src="/user-verification-code/images/03准备captcha扩展包.png" style="zoom:50%">

> 可能出现的错误
* 报错原因：环境中没有Python处理图片的库：**PIL**

<img src="/user-verification-code/images/04安装PIL.png" style="zoom:50%">

> 解决办法
* 安装Python处理图片的库：`pip install Pillow`

### 2. 准备Redis数据库

> 准备Redis的2号库存储验证码数据

```python
"verify_code": { # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
```

### 3. 图形验证码后端逻辑实现

```python
class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码
        text, image = captcha.generate_captcha()

        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图片验证码
        return http.HttpResponse(image, content_type='image/jpg')
```