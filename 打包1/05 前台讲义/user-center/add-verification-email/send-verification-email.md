# 发送邮箱验证邮件

> 重要提示：

* 发送邮箱验证邮件是耗时的操作，不能阻塞美多商城的响应，所以需要**异步发送邮件**。
* 我们继续使用Celery实现异步任务。

### 1. 定义和调用发送邮件异步任务

> **1.定义发送邮件任务**

<img src="/user-center/images/08准备发送邮件异步任务.png" style="zoom:50%">

```python
@celery_app.task(bind=True, name='send_verify_email', retry_backoff=3)
def send_verify_email(self, to_email, verify_url):
    """
    发送验证邮箱邮件
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    """
    subject = "美多商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
    except Exception as e:
        logger.error(e)
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
```

> **2.注册发邮件的任务：main.py**
* 在发送邮件的异步任务中，我们用到了Django的配置文件。
* 所以我们需要修改celery的启动文件main.py。
* 在其中指明celery可以读取的Django配置文件。
* 最后记得注册新添加的email的任务

```python
# celery启动文件
from celery import Celery


# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery实例
celery_app = Celery('meiduo')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
```

> **3.调用发送邮件异步任务**

```python
# 赋值email字段
try:
    request.user.email = email
    request.user.save()
except Exception as e:
    logger.error(e)
    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

# 异步发送验证邮件
verify_url = '邮件验证链接'
send_verify_email.delay(email, verify_url)

# 响应添加邮箱结果
return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})
```

> **4.启动Celery**

```bash
$ celery -A celery_tasks.main worker -l info
```

### 2. 生成邮箱验证链接

> **1.定义生成邮箱验证链接方法**

```python
def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url
```

> **2.配置相关参数**

```python
# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8000/emails/verification/'
```

> **3.使用邮箱验证链接**

```python
verify_url = generate_verify_email_url(request.user)
send_verify_email.delay(email, verify_url)
```
