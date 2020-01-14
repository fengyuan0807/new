# QQ登录工具QQLoginTool

### 1. QQLoginTool介绍

* 该工具封装了QQ登录时对接QQ互联接口的请求操作。可用于快速实现QQ登录。

### 2. QQLoginTool安装

```bash
pip install QQLoginTool
```

### 3. QQLoginTool使用说明

> **1.导入**

```python
from QQLoginTool.QQtool import OAuthQQ
```

> **2.初始化`OAuthQQ对象`**

```python
oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)
```

> **3.获取QQ登录扫码页面，扫码后得到`Authorization Code`**

```python
login_url = oauth.get_qq_url()
```

> **4.通过`Authorization Code`获取`Access Token`**

```python
access_token = oauth.get_access_token(code)
```

> **5.通过`Access Token`获取`OpenID`**

```python
openid = oauth.get_open_id(access_token)
```