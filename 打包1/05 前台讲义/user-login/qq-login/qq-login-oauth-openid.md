# OAuth2.0认证获取openid

> 待处理业务逻辑
 
```   
# 提取code请求参数
# 使用code向QQ服务器请求access_token
# 使用access_token向QQ服务器请求openid
# 使用openid查询该QQ用户是否在美多商城中绑定过用户
# 如果openid已绑定美多商城用户，直接生成JWT token，并返回
# 如果openid没绑定美多商城用户，创建用户并绑定到openid
```

### 1. 获取QQ登录扫码页面

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /qq/login/ |

> **2.请求参数：查询参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **next** | string | 否 | 用于记录QQ登录成功后进入的网址 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **login_url** | QQ登录扫码页面链接 |

> **4.后端逻辑实现**

```python
class QQAuthURLView(View):
    """提供QQ登录页面网址
    https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
    """
    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.GET.get('next')

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url':login_url})
```

> **5.QQ登录参数**

```python
QQ_CLIENT_ID = '101518219'
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'
```

### 2. 接收Authorization Code

> 提示：
* 用户在QQ登录成功后，QQ会将用户重定向到我们配置的回调网址。
* 在QQ重定向到回调网址时，会传给我们一个`Authorization Code`。
* 我们需要拿到`Authorization Code`并**完成OAuth2.0认证获取openid**。
* 在本项目中，我们申请QQ登录开发资质时配置的回调网址为：
    * `http://www.meiduo.site:8000/oauth_callback`
* QQ互联重定向的完整网址为：
    * `http://www.meiduo.site:8000/oauth_callback/?code=AE263F12675FA79185B54870D79730A7&state=%2F`

```python
class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')
        pass
```
```python
url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
```

### 3. OAuth2.0认证获取openid

> 1. 使用code向QQ服务器请求access_token
> 2. 使用access_token向QQ服务器请求openid

```python
class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 提取code请求参数
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')

        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')
        pass
```

### 4. 本机绑定www.meiduo.site域名

> **1.ubuntu系统或者Mac系统**

```bash
编辑 /etc/hosts
```

<img src="/user-login/images/07ubuntu配置域名.png" style="zoom:50%">

<img src="/user-login/images/08Mac配置域名.png" style="zoom:50%">

> **2.Windows系统**

```bash
编辑 C:\Windows\System32\drivers\etc\hosts
```



