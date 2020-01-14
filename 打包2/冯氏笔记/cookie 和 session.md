

# 状态保持：

## cookie：

![1.cookie](C:\Users\FY\Desktop\截图\cookie和session\1.cookie.png)

设置cookies：需要一个HttpResponse类的对象或者它子类的对象，包括：HttpResponseRedirect，JsonResponse

cookie是保存在客户端
cookie是基于域名(IP)的

cookie的特点：
1）以键值对方式进行存储
2）通过浏览器访问一个网站的时候，会将浏览器存储的跟网站相关的所有cookie信息发送给该网站的服务器，request.COOKIES
3)cookie 是基于域名安全的
4)cookie是有过期时间的如果不指定，默认浏览器关闭之后cookie就会过去

第一次请求过程
① 我们的浏览器第一次请求服务器的时候,不会携带任何cookie信息
② 服务器接收到请求之后,发现 请求中没有任何cookie信息
③ 服务器设置一个cookie.这个cookie设置响应中
④ 我们的浏览器接收到这个响应之后,发现响应中有cookie信息,浏览器会将cookie信息保存起来

第二次及其之后的过程
⑤ 当我们的浏览器第二次及其之后的请求都会携带cookie信息
⑥ 我们的服务器接收到请求之后,会发现请求中携带的cookie信息,这样的话就认识是谁的请求了

从http协议角度深入掌握cookie的流程(原理)
 第一次
① 我们是第一次请求服务器,不会携带任何cookie信息,请求头中没有任何cookie信息
② 服务器会为响应设置cookie信息.   响应头中有set_cookie信息

![8](C:\Users\FY\Desktop\截图\cookie和session\8.png)

第二次及其之后的
③ 我们第二次及其之后的请求都会携带cookie信息,请求头中有cookie信息
④(可选) 在当前我们的代码中,没有再 在响应头中设置cookie,所以响应头中没有set_cookie信息

```python
def set_cookie(request):
# 设置cookie信息
response=HttpResponse('设置cookie')
response.set_cookie('num',1,max_age=3600) # 'key':'value'
return response

# 删除cookie的2种方式
# response.delete_cookie(key)
# response.set_cookie(key,value,max_age=0)
    
def get_cookie(request):
# 获取cookie信息
num = request.COOKIES['num']
return HttpResponse(num)

```

## session
![2.seesion](C:\Users\FY\Desktop\截图\cookie和session\2.seesion.png)

保存在服务器的数据叫做 session
session需要依赖于cookie
如果浏览器禁用了cookie,则session不能实现
0.概念
1.流程
第一次请求:
 ① 我们第一次请求的时候可以携带一些信息(用户名/密码) cookie中没有任何信息（带有用户名和密码的post请求的时候）
 ② 当我们的服务器接收到这个请求之后,进行用户名和密码的验证,验证没有问题可以设置session信息
③ 在设置session信息的同时(session信息保存在服务器端).服务器会在响应头中设置一个 sessionid 的cookie信息(由服务器自己设置的,不是我们设置的)
 ④ 客户端(浏览器)在接收到响应之后,会将cookie信息保存起来(保存 sessionid的信息)

第二次及其之后的请求:
⑤ 第二次及其之后的请求都会携带 session id信息
⑥ 当服务器接收到这个请求之后,会获取到sessionid信息,然后进行验证,
验证成功,则可以获取 session信息(session信息保存在服务器端)

3.从原理(http)角度
第一次请求:
① 第一次请求,在请求头中没有携带任何cookie信息
② 我们在设置session的时候,session会做2件事.
#第一件：　将数据保存在数据库中
#第二件：　设置一个cookie信息，这个cookie信息是以　sessionid为key ， value为 xxxxx
cookie肯定会以响应的形式在相应头中出现

第二次及其之后的:
③ 都会携带 cookie信息,特别是 sessionid

cookie和session的区别：

cookie：明文，客户端，5kb   session：加密，服务端，有多大存多大

![session原理图](C:\Users\FY\Desktop\截图\cookie和session\session原理图.png)

```python
def set_session(request):
# 设置session信息
	request.session['username'] = 'smart'
	request.session['age'] = 18 # 这里发送请求，用户名和年龄，进行校验，没有问题服务端自己设置session信息
	return HttpResponse('设置session')

def get_session(request):
# 获取session信息
	username = request.session['username']
	age = request.seesion['age']
	return HttpResponse(username+':'+'str(age)')
```

# csrf

- `CSRF`全拼为`Cross Site Request Forgery`，译为跨站请求伪造。

- CSRF

  指攻击者盗用了你的身份，以你的名义发送恶意请求。

  - 包括：以你名义发送邮件，发消息，盗取你的账号，甚至于购买商品，虚拟货币转账......

- 造成的问题：个人隐私泄露以及财产安全。

发送 127.0.0.0.1/9000的时候，发送一个get请求--->登录页面的get函数--->输入账户和密码，登录页面的post函数------->转账页面的get(生成csrf_token,设置csrf_token到cookie中， csrf_token 保存到表单的隐藏字段中)---->转账页面的post(取出表单中的 csrf_token,取出 cookie 中的 csrf_token)---->服务器

```python
#定义路由
from django.conf.urls  import url
from pay import views
urlpatterns = [
    url(r'^$',views.LoginView.as_view(),name='index'),   #登录路由 
    url(r'^transfer/$',views.TransferView.as_view(),name='transfer'), #转账路由
]

#定义视图
class LoginView(View):

    def post(self,request):

        # 取到表单中提交上来的参数
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not all([username, password]):
            print('参数错误')
        else:
            print(username, password)
            if username == 'laowang' and password == '1234':
                # 状态保持，设置用户名到cookie中表示登录成功
                response = redirect(reverse('transfer'))
                response.set_cookie('username', username)
                return response
            else:
                print('密码错误')
        return render(request,'login.html')
    def get(self,request):
        return render(request,'login.html')

class TransferView(View):


    def post(self,request):
        # 从cookie中取到用户名
        username = request.COOKIES.get('username', None)
        # 如果没有取到，代表没有登录
        if not username:
            return redirect(reverse('index'))
        # 取出表单中的 csrf_token
        form_csrf_token = request.POST.get("csrftoken")
        # 取出 cookie 中的 csrf_token
        cookie_csrf_token = request.COOKIES.get('csrf_token')
        # 进行对比 这个csrf_taoen是设置在返回的响应的cookies中的，得提取出来 跟提交表单（post请求）输入账户和密码的时候，提取模板中的csrf_token作比较
        if cookie_csrf_token != form_csrf_token:
             return HttpResponse('token校验失败，可能是非法操作')

        to_account = request.POST.get("to_account")
        money = request.POST.get("money")

        print('假装执行转操作，将当前登录用户的钱转账到指定账户')
        return HttpResponse('转账 %s 元到 %s 成功' % (money, to_account))

    def get(self, request):
        # 生成csrf_token
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)

        # 渲染转换页面，传入 csrf_token 到模板中
        response = render(request, 'transfer.html',context={'csrf_token':csrf_token})

        # 设置csrf_token到cookie中，用于提交校验
        response.set_cookie('csrf_token', csrf_token)

        return response
```

```python
class TransferView(View):
    def post(self, request):
	# 从cookie中取到用户名
		username = request.COOKIES.get('username', None)

        # 如果没有取到，代表没有登录
        if not username:
            return redirect(reverse('index'))
        # 转账的业务逻辑有错误，需要添加验证
        # user_sms_code = request.POST.get('sms_code')
        # server_sms_code = redis.get('sms_code')，
        # 黑客是获取不到短信验证码的
        user_sms_code = request.POST.get('sms_code')
        server_sms_code = '1234' # 这里是举个例子 ,伪代码
        if user_sms_code != server_sms_code:
            return HttpResponse('不能转账')

        to_account = request.POST.get("to_account")
        money = request.POST.get("money")

        print('假装执行转操作，将当前登录用户的钱转账到指定账户')
        return HttpResponse('转账 %s 元到 %s 成功' % (money, to_account))
```

## 类视图

```
类视图 是采用的面向对象的思路

1.定义类试图
    ① 继承自 View  (from django.views import View)
    ② 不同的请求方式 有不同的业务逻辑
        类试图的方法 就直接采用 http的请求方式的名字 作为我们的函数名.例如: get ,post,put,delete
    ③  类试图的方法的第二个参数 必须是请求实例对象
        类试图的方法 必须有返回值 返回值是HttpResopnse及其子类

2.类试图的url引导
```

```python
# 配置路由时，使用类视图的as_view()方法来添加。
url(r'^login/$',RegisterView.as_view()) # 就是一个view函数名
```

```python
from django.views.generic import View
# 定义类视图需要继承自Django提供的父类View
class RegisterView(View):
    """类视图：处理注册"""

    def get(self, request):
        """处理GET请求，返回注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')
```

```python
@classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        ...省略代码...
		# 请求发送过去,匹配到'login/'路由,触发了view函数,相当于执行view()
        def view(request, *args, **kwargs):
        #  相当于 self =RegisterView() 创建了一个实例对象，cls就是RegisterView
            self = cls(**initkwargs)
            # 以下是初始化方法
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            # 调用dispatch方法，按照不同请求方式调用不同请求方法
            return self.dispatch(request, *args, **kwargs)

        ...省略代码...

        # 返回真正的函数视图
        return view


    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        # 此处request.method 是get方法。
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
```

```python
个人中心页面--必须登陆才能显示
GET 方式 展示 个人中心
POST 实现个人中心信息的修改
定义类视图
from django.contrib.auth.mixins import LoginRequiredMixin
# mro顺序 继承
# LoginRequireMixin 里面有个登录判断的方法
class CenterView(LoginRequireMixin,View):

    def get(self,request):
        return HttpResponse("OK")

    def post(self,request):
        return HttpResponse("OK")
```

static_test = blocked_ips(static_test)

static_test()

## 中间件

定义：Django中的中间件是一个轻量级、底层的插件系统，可以介入Django的请求和响应处理过程，修改Django的输入或输出。中间件的设计为开发者提供了一种无侵入式的开发方式，增强了Django框架的健壮性。

作用：我们可以使用中间件，在Django处理视图的不同阶段对输入或输出进行干预。

```python
# get_response 视图函数

# 中间件的作用：每次请求和响应的时候后都会被调用

def simple_middleware(get_response):
    #**** 此处编写的代码仅在Django第一次配置和初始化的时候执行一次。
	def middleware(request):
    # 此处编写的代码会在每个请求处理视图前被调用。
    	response = get_response(request)
    # 此处编写的代码会在每个请求处理视图之后或者响应之后被调用。
    	return response
	return middleware
```
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.my_middleware',  # 添加 记得加逗号
    'users.middleware.my_middleware2',  # 添加
]
```

## 多个中间件的执行顺序

- 在请求视图被处理**前**，中间件**由上至下**（按照注册的顺序）依次执行
- 在请求视图被处理**后**/响应后，中间件**由下至上**依次执行

