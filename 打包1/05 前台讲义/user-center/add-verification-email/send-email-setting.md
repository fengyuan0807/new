# Django发送邮件的配置

<img src="/user-center/images/07邮箱验证邮件.png" style="zoom:50%">

### 1. Django发送邮件流程分析

<img src="/user-center/images/05Django发送邮件流程.png" style="zoom:50%">

> `send_mall()`方法介绍
*  位置：
    * 在`django.core.mail`模块提供了`send_mail()`来发送邮件。
* 方法参数：
    * `send_mail(subject, message, from_email, recipient_list, html_message=None)`
    
```
subject 邮件标题
message 普通邮件正文，普通字符串
from_email 发件人
recipient_list 收件人列表
html_message 多媒体邮件正文，可以是html字符串
```

### 2. 准备发邮件服务器

> **1.点击进入《设置》界面**

<img src="/user-center/images/06准备发邮件服务器1.png" style="zoom:50%">

> **2.点击进入《客户端授权密码》界面**

<img src="/user-center/images/06准备发邮件服务器2.png" style="zoom:50%">

> **3.开启《授权码》，并完成验证短信**

<img src="/user-center/images/06准备发邮件服务器3.png" style="zoom:50%">

> **4.填写《授权码》**

<img src="/user-center/images/06准备发邮件服务器4.png" style="zoom:50%">

> **5.完成《授权码》设置**

<img src="/user-center/images/06准备发邮件服务器5.png" style="zoom:50%">

> **6.配置邮件服务器**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.163.com' # 发邮件主机
EMAIL_PORT = 25 # 发邮件端口
EMAIL_HOST_USER = 'hmmeiduo@163.com' # 授权的邮箱
EMAIL_HOST_PASSWORD = 'hmmeiduo123' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<hmmeiduo@163.com>' # 发件人抬头
```

