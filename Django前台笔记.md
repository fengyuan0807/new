# 使用乐观锁并发下单

> **重要提示：**

- 在多个用户同时发起对同一个商品的下单请求时，先查询商品库存，再修改商品库存，会出现资源竞争问题，导致库存的最终结果出现异常。

### 1. 并发下单问题演示和解决方案

![img](../images/04并发下单问题演示.png)

> **解决办法：**

- 悲观锁

  - 当查询某条记录时，即让数据库为该记录加锁，锁住记录后别人无法操作，使用类似如下语法

    ```python
    select stock from tb_sku where id=1 for update;
    
    SKU.objects.select_for_update().get(id=1)
    ```

  - 悲观锁类似于我们在多线程资源竞争时添加的互斥锁，容易出现死锁现象，采用不多。

- 乐观锁

  - 乐观锁并不是真实存在的锁，而是在更新的时候判断此时的库存是否是之前查询出的库存，如果相同，表示没人修改，可以更新库存，否则表示别人抢过资源，不再执行库存更新。类似如下操作

    ```python
    update tb_sku set stock=2 where id=1 and stock=7; # stock=7 原始库存
    
    result= SKU.objects.filter(id=1, stock=7).update(stock=2) # 如果在更新数据时，原始数据变化了，返回0，表示有资源抢夺
    ```

- 任务队列

  - 将下单的逻辑放到任务队列中（如celery），将并行转为串行，所有人排队下单。比如开启只有一个进程的Celery，一个订单一个订单的处理。

```python
while True:
    # 乐观锁更新库存和销量
    new_stock = origin_stock - sku_count
    new_sales = origin_sales + sku_count
    result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
    # 如果下单失败，但是库存足够时，继续下单，直到下单成功或者库存不足为止
    if result == 0:
        continue
```

### django中的事务：

> **重要提示：**

- 在保存订单数据时，涉及到多张表（OrderInfo、OrderGoods、SKU、SPU）的数据修改，对这些数据的修改应该是一个整体事务，即要么一起成功，要么一起失败。
- Django中对于数据库的事务，默认每执行一句数据库操作，便会自动提交。所以我们需要在保存订单中自己控制数据库事务的执行流程。

### 1. Django中事务的使用

> **1.Django中事务的使用方案**

- 在Django中可以通过**django.db.transaction模块**提供的**atomic**来定义一个事务。

- **atomic**提供两种方案实现事务：

  - 装饰器用法：

    ```python
    from django.db import transaction
    
    @transaction.atomic
    def viewfunc(request):
      # 这些代码会在一个事务中执行
      ......
    ```

  - with语句用法：

    ```python
    from django.db import transaction
    
    def viewfunc(request):
      # 这部分代码不在事务中，会被Django自动提交
      ......
    
      with transaction.atomic():
          # 这部分代码会在事务中执行
          ......
    ```

> **2.事务方案的选择：**

- **装饰器用法：**整个视图中所有MySQL数据库的操作都看做一个事务，范围太大，不够灵活。而且无法直接作用于类视图。
- **with语句用法：**可以灵活的有选择性的把某些MySQL数据库的操作看做一个事务。而且不用关心视图的类型。
- 综合考虑后我们选择 **with语句实现事务**

> **3.事务中的保存点：**

- 在Django中，还提供了保存点的支持，可以在事务中创建保存点来记录数据的特定状态，数据库出现错误时，可以回滚到数据保存点的状态。

```python
from django.db import transaction

with tansaction.atominc():
    # 创建保存点
    save_id = transaction.savepoint()  
    # 回滚到保存点
    transaction.savepoint_rollback(save_id)
    # 提交从保存点到当前状态的所有数据库事务操作
    transaction.savepoint_commit(save_id)
```

### 用户订单

```python
判断pay_method是否合法
if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'] ,OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
    return http.HttpResponseForbidden('pay_method错误')
保存订单基本信息（一）

保存订单商品信息（多）
sku_ids=new_cart_dict.keys()
for sku_id in sku_ids:
	sku=SKU.objects.get(id=sku_id) # 查询商品和库存信息时，不能出现缓存，所以没用filter（id__in=sku_ids）
```



freight = Decimal(10.00) 高精度浮点型的数据写法

toutoal_amount = Decimal(0.00)

**foreignKey外键对应的字段都是id**，不是name

### 用户中心

邮箱验证：补充用户模型类字段 email_active 。

添加字段，需要给默认值。

修改表结构，增加字段的话 需要make migrations

有了迁移文件，只需要迁移的话make migrate

**如果 LoginRequiredMixin 判断出用户已登录，那么request.user 就是登录用户。**

```
修改邮件字段： 
def put（self，request）
	json_dict = json.loads(request.body.decode())
```

### 发邮件

```
from django.core.mail import send_mail

send_mail(subject, message, from_email, recipient_list, html_message=None)
# subject 邮件标题
# message 普通邮件正文，普通字符串
# from_email 发件人
# recipient_list 收件人列表
# html_message 多媒体邮件正文，可以是html字符串
```

### QQ登录：

```
pip install itsdangerous
openid需要签名 补充itsdangerous的使用,使用TimedJSONWebSignatureSerializer可以生成带有有效期的token,可逆

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

serializer = Serializer(settings.SECRET_KEY, 300) # serializer = Serializer(秘钥, 有效期秒)
data = {'openid': openid}
token = serializer.dumps(data) # serializer.dumps(数据), 返回bytes类型
return token.decode()


# 验证失败，会抛出itsdangerous.BadData异常
serializer = Serializer(settings.SECRET_KEY, 300)
try:
    data = serializer.loads(token)
except BadData:
    return None
return data.get('openid')
```



```
使用openid判断该QQ用户是否绑定过美多商城的用户
oauthqquser = OAUthQQuser.objects.get(openid=openid)

把openid放在前端form表单中存放
```

登录工具：

QQ登录攻略：<https://wiki.connect.qq.com/%E5%BC%80%E5%8F%91%E6%94%BB%E7%95%A5_server-side>

BaseModel 模型类（基类）

```
class Meta:
	abstract=True		#	说明是抽象模型类,不单独建表，⽤于继承使⽤，数据库迁移时不会创建BaseModel的表
```

#### 首页、我的订单等等右上角展示用户名

```
用缓存来做，从cookie中拿取用户名
# request.set_cookie('key',value,'expiry')
response.set_cookie('username', user.username,max_age=3600)
```

```
认证用户：使用账号查询用户是否存在，如果用户存在，再校验密码是否正确。

自己写的方法:
user= User.object.get(username=username)
user.check_password(password=password)

但是django帮我们封装好了，使用账号查询是否存在，只能通过用户名认证用户，如果用户名存在，再校验密码是否正确,都正确，返回user
from django.contrib.auth import authenticate
user = authenticate(username=username,password=password,**kwargs)
```

#### 状态保持

本质是实现session的保持，⽤户登录的本质： 状态保持 将通过认证的⽤户的唯⼀标识信息（⽐如：⽤户ID）写⼊到当前浏览器的 cookie和服务端的 session 中。注：cookie = request.COOKIES.get('itcast')

```
response.set_cookie('username', user.username,max_age=3600)只是为了在界面上面显示用户名.
```

- login(request,user) 封装了写入session的操作,状态保持需要用户模型类对象

  - 是否记住登录：

  - 不记住登录，浏览器会话结束就销毁

    ```
    if rememberd ！='on'
    	request.session.set_expiry(0)
    ```

  - 记住登录，状态保持两周

    ```
    else:
    	request.session.set_expiry(None) # 默认是两周
    ```

- logout(request) 封装了清理session的操作

  ```
  response.delete_cookie('username')
  ```

#### 自定义用户认证方法：用于账号登录

因为自带的封装的方法，只能通过用户名(username)认证用户authenticate

所以要自定义认证方法，通过用户名或者手机号认证用户。

```
多账户认证：通过用户名或者是手机号认证用户，所以要重写用户认证后端

from django.contrib.auth.backends import ModelBackend
from .models import User

def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名或者手机号
    :return: user
    """
    #try:
    #   user = User.objects.get(username=account)
    #except User.DoesNotExist:
    #    try:
    #        user = User.objects.get(mobile=account)
    #    except User.DoesNotExist:
    #        return None
    #return user
	try:
		# 手机号可以登录，用户名也可以登录
        user = User.objects.get(Q(username=account)|Q(mobile=account))
       # user = User.objects.filter(Q(username=account)|Q(mobile=account))[0]
    except User.DoesNotExist:
        return None
    return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端，实现多账号登录"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据传入的username获取user对象。username可以是手机号也可以是账号
        user = get_user_by_account(username)
        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user
        else：
        	return None
          
# 在配置文件中添加
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']
```

```
response.set_cookie('username',user.username,max_age=3600)
user.username 是当前认证用户的用户名所以不写username
```

## verifications 验证子应用

> 注：运行一个单独的py文件，而该py文件中需要使用Django中的东西，则需要在py文件的开头添加以下代码：

```python
在发送邮件的异步任务中，我们用到了Django的配置文件。
所以我们需要修改celery的启动文件main.py。
在其中指明celery可以读取的Django配置文件。
最后记得注册新添加的email的任务

# 设置Django运行所依赖的环境变量
import os
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
  # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_demo.settings')
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
 # 如果更改了setting的位置 写成这样

# 让Django进行一次初始化
import django
django.setup() 
```

####  celery异步方案 （异步来做，从主业务中解耦出来）

**发送短信验证码**

**发邮件** :发送邮箱验证邮件是耗时的操作，不能阻塞美多商城的响应，所以需要**异步发送邮件**。

- 生产者消费者设计模式：
  - 生产者---> 消息队列（broker）<---消费者
    ​        任务/消息：发送短信
    ​        生产者：美多商城
    ​        消费者：Celery
    ​        中间人：任务/消息队列
    - 1、单个celery进程每分钟可以处理数以百万计的任务，生产者消费者设计模式全部封装好了
    - 2、简单可靠灵活非分布式系统可以在多台或者一台机器上运行
      ​	pip install -U Celery

```
mian.py config.py tasks.py


容器：redis数据库
# config.py里写：
broker_url = 'redis://192.168.182.128/10'


# mian.py里写
from celery import Celery
# 创建celery实例子
celery_app = Celery('meiduo')
# 加载配置
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])


# tasks.py
# 定义任务：发送短信验证码 task 是个函数,使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile,sms_code)：
	ret = CCP().send_template_sms(mobile,[sms_code,5],1)
	return ret
	
# tasks.py	
from django.core.mail import send_mail
send_mail(subject, message, from_email, recipient_list, html_message=None)
# subject 邮件标题
# message 普通邮件正文，普通字符串
# from_email 发件人
# recipient_list 收件人列表
# html_message 多媒体邮件正文，可以是html字符串

# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
@celery_app.task(bind=True, name='send_verify_email', retry_backoff=3)
def send_verify_email(self, to_email, verify_url):
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

celery -A celery_tasks.main worker -l info
-A 指定对应的应用程序，是项目中celery实例的位置

# 发送短信验证码 使用celery发送短信验证码
from celery_tasks.sms.tasks import send_sms_code
send_sms_code.delay(mobile,sms_code) #千万不要忘记写delay
send_verify_email.delay(email, verify_url)
```

#### pipline（管道）操作redis数据库（网络操作都有延时）

```
提升redis数据库（C-S架构）操作的效率
redis处理多个请求，同时是以阻塞模式，等待服务端的响应
一、好处：
    1、可以一次性发送多条命令，并在执行完后，一次性将结果返回
    2、通过减少客户端与redis的通信次数来实线降低往返延时时间
二、实现原理：
    1、原理是队列
    2、Client可以将三个命令放到一个tcp报文一起发送
    3、Server则可以将三条命令的处理结果放到一个tcp报文返回
    4、队列是先进先出保证数据的顺序性
三、步骤：
    1、创建管道
    pl = redis_conn.pipline()
    2、将命令添加到队列
    pl.setex(。。。。)
    3、执行
    pl.execute()
```

#### 避免频繁发送短信验证码

```python
在redis数据库中设置一个标记，可以设置有效期
send_flag_mobile:1
# 保存短信验证码
# 顺便保存标记
redis_conn.setex('send_flag_%s' % mobile,300,1)
```

#### 导包

配置环境的写到上面，自己的，空一行写在下面

#### 日志器

```python
import logging
logger = logging.getlogger()
logger.info(sms_code) # 手动输出日志
```

#### 大写转小写

```
lower()方法
```

#### redis 数据库

存入到redis的数据是bytes类型，解码decode()

```python
image_code_server.decode()
setex('sms_%s' % mobile,300,sms_code)
import random
sms_code = '%06d' % random.randint(0,999999)  随机六位数字
300/60=5.0
300//60=5
```

#### 单例

什么是单例？ hasattr()方法：判断某个对象是否有某个属性 

单例模式即一个类有且仅有一个实例

```python
比如宇宙只有一个地球：
class Earth(object):
	pass
a = Earth()
b = Earth()
print(id(a)) # 935478784072
print(id(b)) # 935478784184
通过打印实例的id可以发现，地球类默认创建了两个实例。
那么怎么能够让类只创建一个实例，而后再创建的实例是返回上一次的对象的引用呢？
那么以下5中单例写法：
1、通过改写__new__方法实现（推荐）
class Single(object):
    def __new__(cls, *args, **kwargs):
        # _instance属性中存储的就是单例，判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例  （hasattr方法：判断某个对象是否有某个属性） _instance(前面有下划线，私有的实例)
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class A(Single):
    pass
a = A()
b = A()
print('a的id是：', id(a))
print('b的id是：', id(b))

2、通过装饰器
def SingleTon(cls, *args, **kwargs):
    #instance作为字典变量写在外部,可以保证该装饰器的重用性
    _instances = {}
    def singleton():
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return singleton

@SingleTon
class TestClass(object):
    a = 1

test1 = TestClass()
test2 = TestClass()

print test1.a ,test2.a
test1.a = 2
print test1.a ,test2.a
print id(test1),id(test2)
————————————————
或者这么写
def dector(cls, *args, **kwargs):
    def inner():
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    return inner

@dector
class A(object):
    pass

a = A()
b = A()
print('a的id是：', id(a))
print('b的id是：', id(b))


3、使用元类
class SingleTon(type):
    _instance=None #此处可改为_instances = {}字典实现
    def __call__(cls, *args, **kwargs):
        if not cls._instance : #条件相应得改为 not cls in _instances
            cls._instance = cls.__call__(cls,*args, **kwargs)
           # _instance[cls]=cls.__new__(cls,*args, **kwargs) #若instances为字典,则_instances[cls] = cls.__new__(cls,*arg,**kwarg)
        return cls._instance

class TestClass(object):
    __metaclass__ = SingleTon

test1 = TestClass()
test2 = TestClass()

test1.a = 1
print test1.a ,test2.a
test1.a = 2
print test1.a ,test2.a
print id(test1),id(test2)
————————————————
4：共享属性
class SingleTon(object):
    _state = {}
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._state
        return obj

class TestClass(SingleTon):
    a = 1

print test1.a ,test2.a
test1.a = 2
print test1.a ,test2.a
print id(test1),id(test2)
————————————————
5、Python模板
class My_SingleTon(object):
    def foo(self):
        pass
my_sign = My_SingleTon()

my_sign.foo()
```



### 默认的用户模型类

地址：django--contrib--auth--models.py

导包：

```python
from djano.contrib.auth.models import AbstractUser
# 自定义用户模型类
class User(Abstractuser):
    mobile = models.CharField等等
```

基本属性：

- 创建用户（注册用户）必选：username，password

- 判断用户是否通过认证（登录）：is_authenticated,
  - 注意：判断用户是否登录，django提供了一个属性名是is_authenticated，真正使用的时候用了一个扩展类：LoginRequiedMixin

### 查询用户是否存在

user = User.objects.get(mobile=mobile)

### 新建用户（保存用户数据）

- 如果是自己定义的用户模型类User：创建新用户方法是：
  - User.object.create_user(username=username,password=password,mobile=mobile)
  - 这⾥使⽤Django认证系统⽤户模型类提供的 create_user() ⽅法创建新的⽤户。 这⾥	create_user()	⽅法中封装了	set_password() ⽅法加密保存密码，保存到数据库。
- 如果不是自己定义的用户模型类：创建新用户方法是：
  - OAuthQQUser.objects.create(user=user,openid=openid)

### 校验密码

user.check_password(password)

### 设置密码

user.set_password(password) 加密的



## 用户中心:

#### 只有用户登录了才能进到用户中心,我的订单，用到LoginRequiredMixin，作为视图的父类，一定要写在第一个。

### 判断用户是否登录

判断用户是否登录，django提供了一个属性名是is_authenticated

真正使用的时候用了一个扩展类：LoginRequiedMixin，用户未登录用到handel_no_permission方法，用户登录的话，走到super方法中

```python
class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""
# LoginRequiredMixin，判断用户是否登录，如果登录了才会进入函数（视图）内部
#1、只有类试图中用了LoginRequiredMixin之后，request.user取出来的才是登录用户
#2、如果没有用LoginRequiredMixin
    def get(self, request):
        """提供个人信息界面"""
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context=context)
```

- LoginRequiredMixin（判断用户是否登录）

- 为什么要使用LoginRequiredMixin

```python
原始写法，是我们自己写的：
if request.user.is_authenticated:
   return render(request,'user_center_info.html')
else:
   return redirect(reverse('users:login'))
```

  - 1、如果用原始写法体现的只是一个过程，并不是结果，并不是封装，这个代码会被用到很多地方，所以我们的django就被封装到LoginRequiredMixin，

  - 2、原始写法太粗燥，稍微复杂的功能就不能实现了，LoginRequiredMixin也扩展了一些方法，
    - 帮我们封装了用户登录认证的代码。并且能够记录重定向的地址。

### 自定义LoginRequiedJsonMixin类

  ```python
因为LoginRequiredMixin，最后返回的是return HTTPResponseRedirect，所以要自定义LoginRequiredJsonMixin扩展类继承因为LoginRequiredMixin，判断用户是否登录
  class LoginRequiredJSONMixin(LoginRequiredMixin):
      """Verify that the current user is authenticated."""
  # handle_no_permission说明：我们只需要改写父类中的处理方式 至于如何判断用户是否登录 在父类中已经判断了
      def handle_no_permission(self):
          return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
  ```


```
class UserInfoView(LoginRequiredMixin,View):

# 1、login_url = '/login/' # 判断用户是否登录，用户未登录用户的重定向（跳转）的地址，这个一般写在settings中的dev文件中：LOGIN_URL = '/login/'

# 2、redirect_field_name = 'redirect_to' # 用户登录成功回到哪个地方，默认是'next'，但是这个next必须是我们来写
```

```
登录完了之后，指定用户登录后重定向的地址，
- 如果有next，指向next指向的页面
- 如果没有next，进到首页，但是这部分的next需要我们自己做，从哪里来跳到哪里去
next = request.GET.get('next')
if next:
	 response = redirect(next)
else:
	 response = redirect(reverse('contents:index'))
```

```

- 怎么使用LoginRequiredMxin？

- 先继承LoginRequiredMixin，后继承View。

- LoginRequiredMixin的原理是什么？？

   ![11](\img\11.png)

- LoginRequiredMixin   的  next参数的使用

 认证用户：Django自带的用户认证系统只会使用用户名去认证一个用户。

- 所以我们为了实现多账号登录，就可以自定义认证后端，采用其他的唯一信息去认证一个用户。

```


### 添加邮箱,修改字段

```python
request.user.email = email
request.user.save()

user.email_active = True
user.save()
```

### 修改字段

```
address.is_deleted = True
address.save()
```


​        

## get和filter区别

### OAUthQQuser.objects.get(openid=openid)

OAUthQQuser.objects.get(openid=openid) 

- 查询的是对象
- 对应的查询是一整条记录
- 查的不是user_id也不是open_id,

![OAUTHUSER.OBJECTS.get(openid=openid)](\img\OAUTHUSER.OBJECTS.get(openid=openid).png)



- 输入参数：

get的参数只能是model中定义的哪些字段，只支持严格匹配

filter的参数可以是字段也可以是扩展的where查询关键字，如in，like

- 返回值：

get返回值是一个定义的model对象，是一个模型对象

```
>>> BookInfo.objects.get(id=1)
<BookInfo: 射雕英雄传>
```

filter返回值是一个新的QuerySet对象，是一个模型对象列表

```
>>> BookInfo.objects.all()
<QuerySet [<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>, <BookInfo: 笑傲江湖>, <BookInfo: 雪山飞狐>]>
```

然后可以对QuerySet在进行查询返回新的QuerySet对象，模型列表，支持链式操作，QuerySet一个集合对象，可使用迭代或者遍历，切片等，但是不等于list类型（是一个object对象集合）

### 当渲染页面的时候，需要记住什么时候转字典，什么时候不需要转字典？

- 当使用vue渲染页面或者响应Ajax请求的时候需要转字典

- 当使用Django模板引擎或者jinja2模板引擎渲染页面时候不需要转字典

return http.JsonResponse({'code':'ok','errmsg':'ok','province_list':province_list})

JsonResponse、vue 只认识列表字典或者字典列表 不认识模型列表，只有Django和jinja2模板引擎认识，所以需要把模型列表转成字典列表

- update

使用模型类.objects.filter(id=address_id).update(user=request.user,title=receiver........),会返回受影响的行数

再查一下使用模型类.objects.get(id=address_id)

- 异常：

get只有一条记录返回的时候才正常，也就是说明get查询字段必须是主键或者唯一约束的字段。当返回多条记录或者没有找到记录的时候都会抛出异常

**get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错，有多条记录也会报错。**

**filter有没有匹配的记录都可以，**

**filter方法是从数据库的取得匹配的结果，返回一个对象列表查询集QuerySet ，而不是简单的列表，如果记录不存在的话，它会返回[ ]。**

```
>>> books = BookInfo.objects.filter(readcount__gt=30).order_by('pub_date')
>>> books
<QuerySet [<BookInfo: 天龙八部>, <BookInfo: 雪山飞狐>]>
```

```python
province_model_list = Area.objects.filter(parent_id__isnotnull=True)
province_list = []
for province_model in province_model_list:
province_list.append({'id': province_model.id, 'name': province_model.name})
```

```python
上面一个代码块等价于：（列表推导式）province_list = [{'id':province_model.id,'name':province_model.name} for province_model in province_model_list]:                  
```

```
province_model = Area.objects.get(id=parent_id)
subs_model_list = province_model.area_set.all() # province_model.subs.all()
```



# 异常

![捕获异常](img\捕获异常.png)

User.objects.filter(username=username).count()

filter 查出来的是结果集

get查出来的是对象

### 返回图形验证码
    return http.HttpResponse(image, content_type='image/jpg')

发送短信验证码过于频繁,设置一个标记为1的

```
send_flag_mobile = redis_conn.setex('send_flag_%s' % mobile,600,1)
```



### qq登录：state=next 一直存在的 只需要传一次

except OAuthQQUser.DoesNotExist:

     return http.HttpResponseServerError('OAuth2.0认证失败')
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            #openid没有绑定用户
            pass
        else:
            #openid已经绑定的用户。oauth_user.user 表示从QQ登录模型类中找到对应的用户模型类对象
            login(request,oauth_user.user)
            response = redirect(reverse('content:index'))
            response.set_cookie('username', oauth_user.user.username, max_age=3600)
          	return response
   #### 首页显示用户名信息，需要缓存到cookie
    user = authenticate(username=username, password=password)
    # 这个user是经过认证的user，所以username也是user.username,经过认证的用户的用户名
    response.set_cookie('username', user.username, max_age=3600)

****

将用户地址模型列表转字典列表：因为jsonresponse和vue不认识模型列表，只有django和jinja2模板引擎认识

### 用户中心——展示收货地址

```bash
mysql -h数据库ip地址 -u数据库用户名 -p数据库密码 数据库 < areas.sql
mysql -h127.0.0.1 -uroot -pmysql meiduo_mall < areas.sql
```

####  查询省份数据

```django
Area.objects.filter(属性名__条件表达式=值)
province_model_list = Area.objects.filter(parent__isnull=Ture)  # 查询的是模型对象列表
或者 Area.objects.filter(parent_id__isnull=Ture)

queryset = GoodsCategory.objects.filter(parent=None)

[<Area:北京市>,<Area:天津市>,<Area:山西省>,<Area:江苏省>......]
这个对象列表可使用迭代或者遍历，切片等，但是不等于list类型（是一个object对象集合）
```

**当渲染页面的时候，需要记住什么时候转字典，什么时候不需要转字典？**

- 当使用vue渲染页面或者响应Ajax请求的时候需要转字典
- 当使用Django模板引擎或者jinja2模板引擎渲染页面时候不需要转字典

return http.JsonResponse({'code':'ok','errmsg':'ok','province_list':province_list})

**JsonResponse**、**vue 只认识列表字典或者字典列表 不认识模型列表，只有Django和jinja2模板引擎认识，所以需要把模型列表转成字典列表。**

#### 查询市或区数据

```django
parent_model  = Area.objects.get(id=area_id) # 一查多 模型类名小写_set.all()
sub_model_list = parent_model.subs.all()
```

查询集：QuerySet  从数据库中获取的对象的集合，这些方法会放回查询集

- all()
- filter()
- exclude()
- order_by()

## 缓存服务：

### 1、Redis也可以做缓存，但是取出来的数据是byte类型的

### 2、cache做缓存的话：存储进去和读取出来的数据类型相同，所以读取出来后可以直接使用。默认存储到redis数据库的default数据库的0号库中 

- 省市区数据是我们动态查询的结果
- 但是省市区数据不是频繁变化的数据，所以没有必要每次都要重复查询
- 所以我们可以选择对省市区数据进行缓存处理

```
缓存工具：from django.core.cache import cache
存储缓存数据：cache.set('key'，内容，有效期)
读取缓存数据：cache.get('key')
删除缓存数据：cache.delete('key')
```

#### 一、新增地址：

```python
class Address(BaseModel):
	city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, 	related_name='city_addresses', verbose_name='市')

Address模型类中的外键指向areas/models里面的Area。指明外键时，可以使用应用名.模型类名来定义。

class User(AbstractUser):
	default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')
    这个地方的Address 也可以不加引号
```

`ordering = ['-update_time']` : 根据更新的时间倒叙。

- post

json_dict = json.loads(request.boday.decode())

```python
address = Address.objects.create( # create方法封装了save()方法
	user=request.user，
    title=receiver，
	......
) 
if not request.user.default_address:
    request.user.default_address_id=address.id  # 记住以后就用字段default_address_id 
```

```django
# 判断用户地址是否超过上限 
两种方法：
count = request.user.addresses.count() # 一查找多，高级查询方式，使用related_name 查询
count = Address.objects.filter(user=request.user).count() # 基础查询方式
展示地址：
addresses = Address.objects.filter(user=request.user,is_deleted=False)
```

#### 二、展示收货地址：

- get

1、获取当前登录用户对象

2、使用当前登录用户和is_deleted=Fales作为条件查询地址数据

```python
addresses = Address.objects.filter(user=request.user,is_deleted=True) # 模型对象列表
```

3、将用户地址模型列表转字典列表

```js
# vue只认识js数据，所以需要将模板渲染的数据先给到js，让vue去读js中的数据
<script type="text/javascript">
		let addresses = {{ addresses | safe }};
		let default_address_id = {{ default_address_id }};
</script>
```

#### 三、修改地址（更新）

- put
- 使用最新的地址信息覆盖指定的旧的地址信息

```python
Address.objects.filter(id=address_id).update(  # 返回的是受影响的行数,get 返回的是一个对象
	user = request.user，
    province_id = province_id,
    city_id = city_id,
    district_id = district_id,
    。。。。
)  
address= Address.objects.get(id=address_id) # 所以只能自己查一个

第二种方式：
address = Address.objects.get(id=address_id)
address.title=''
address.user=''
address.save()
```

####  四、删除地址：

- delete

```python
address= Address.objects.get(id=address_id)
address.is_deleted=True
address.save()
```

#### 五、设置默认地址：

- put

```python
address= Address.objects.get(id=address_id)
request.user.default_address=address
request.user.save()
```

#### 六、更新地址标题

- put

```python
address= Address.objects.get(id=address_id)
address.title = title
address.save()
```

### 查询首页商品分类

SPU与SKU:一对多

通俗的讲，属性值、特性相同的商品就可以归类到一类SPU。

通俗的讲，SKU是指一款商品，每款都有一个SKU，便于电商品牌识别商品。库存量单位。

- 首页商品分类数据结构

  ```json
  {
      "1":{
          "channels":[
              {"id":1, "name":"手机", "url":"http://shouji.jd.com/"},
              {"id":2, "name":"相机", "url":"http://www.itcast.cn/"}
          ],
          "sub_cats":[
              {
                  "id":38, 
                  "name":"手机通讯", 
                  "sub_cats":[
                      {"id":115, "name":"手机"},
                      {"id":116, "name":"游戏手机"}
                  ]
              },
              {
                  "id":39, 
                  "name":"手机配件", 
                  "sub_cats":[
                      {"id":119, "name":"手机壳"},
                      {"id":120, "name":"贴膜"}
                  ]
              }
          ]
      }
  }
  ```

- 查询商品分类频道数据

```python
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = OrderedDict()
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        for channel in channels:
            group_id = channel.group_id  # 当前组

            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            cat1 = channel.category  # 当前频道的类别

            # 追加当前频道
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url # 数据结构中需要一个字段是url 所以万不得已自己构造出来
            })
            # 构建当前类别的子类别
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []  # python是一个面向对象的语言，数据结构中二级类别有个字段是‘sub_cats' 是个列表类型的，所以自己来构造
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3) # 这里直接可以把cat3 放进来是因为商品类别表中有id、name的字段
                categories[group_id]['sub_cats'].append(cat2)

        # 渲染模板的上下文
        context = {
            'categories': categories,
        }
        return render(request, 'index.html', context)
```

### 查询首页广告数据

```python
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""

        # 广告数据
        contents = {}
        # 查询所有的广告类别
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            # 使用广告类别查询出该类别对应的所有的广告的内容 一查多 多的模型类名小写_set
            contents[cat.key]= cat.content_set.filter(status=True).order_by('sequence')
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)
```

### 搜索

- [Elasticsearch](https://www.elastic.co/) 的底层是开源库 [Lucene](https://lucene.apache.org/)。但是没法直接使用 Lucene，必须自己写代码去调用它的接口。

思考：

- 我们如何对接 Elasticsearch服务端？

解决方案：

- **Haystac**

我们使用Docker 相同的事情没必要重复做，避免相同的工作重复做是容器化技术应用之一

### FastDFS

- FastDFS的安装步骤非常的多，涉及的依赖包也很多，当新的机器需要安装FastDFS时，是否需要从头开始安装。
- 我们在学习时拿到ubuntu系统的镜像，在VM虚拟机中运行这个镜像后，为什么就可以直接进行开发，而不需要重新搭建开发环境。
- 在工作中，如何高效的保证开发人员写代码的开发环境与应用程序要部署的生产环境一致性。如果要部署一台新的机器，是否需要从头开始部署。
- 所以也用Docker来安装

### 图片加载不出来的话记得看

```bash
看redis是否启动
cd /etc/redis
sudo redis-server redis.conf
重启数据库
sudo service mysql stop
（restart、start）
重启docker
sudo service docker  restart
查看正在运行的容器
sudo docker container ls
查看所有的容器
sudo docker container ls --all
# 启动容器
$ sudo docker container start 容器名或容器id
 tracker storage
如果无法重启storage容器，可以删除/var/fdfs/storage/data目录下的fdfs_storaged.pid 文件，然后重新运行storage。
cd /var/fdfs/storage/data
rm fdfs_storage.pid
主从的mysql服务器都要开 
mysql-slave 在docker中
```

### 浏览记录存储方案

```
Redis中的list类型存储 sku_id，存储类型：'history_user_id' : [sku_id_1, sku_id_2, ...]
lrange 取出列表中所有的数据
```

### 购物车操作：

```
用户、商品、数量：hash
carts_user_id: {sku_id1: count, sku_id3: count, sku_id5: count, ...}
勾选状态：set
只将已勾选商品的sku_id存储到set中，比如，1号和3号商品是被勾选的。
selected_user_id: [sku_id1, sku_id3, ...]

cookies的字典数据
{
    "sku_id1":{
        "count":"1",
        "selected":"True"
    },
    "sku_id3":{
        "count":"3",
        "selected":"True"
    },
    "sku_id5":{
        "count":"3",
        "selected":"False"
    }
}
```



```
user = request.user(匿名用户)
if user.is_authenticated:# 判断用户是否登录
```

设置、修改的时候操作redis数据库的话：redis_conn.pipline( )      pl.execute( ) 读的时候不需要

没有错就忽略所以不需要try

从cookies中读取数据：request.COOKIES.get('carts')

**str_to_dict： encode()-->base64.b64decode()-->pickle.loads()**

**dict_to_str:    pickel.dumps()-->base64.b64encode()-->decode()**

- **isinstance（对象，类型）判断对象是否是这个类型的**

pl 在设置的时候需要些，但是在读取的时候不需要

#### 1、新增数据：

- hincrby key field increment :如果key不存在，则会新建一个新的哈希表，key存在的话，在原有的基础上做增量计算
- pl.hincrby('carts_%s' % user.id, sku_id, count)
- sadd key memeber 如果key不存在，则会新建一个集合，如果member已经存在，自动忽略
- pl.sadd('selected_%s' % user.id, sku_id)

判断key 在不在dict中：if key in dict：..../if key in dict.keys 

####  2、查询数据：

- hgetall key 返回所有的域和值 返回的是字典 # {b'1':b'20',b'2':b'30',b'3':b'50'}
- redis_cart = redis_conn.hgetall('carts_%s' % user.id)
- smembers key 返回集合key中对应的members 返回的是列表 # [b'1,b'2']
- cart_selected = redis_conn.smembers('selected_%s' % user.id)

#### 3、修改数据：

- 后端接收最终的数据，所以覆盖写入，用户登录和不登录都一样覆盖写入 
- hset key field value
- pl.hset('carts_%s' % user.id, sku_id, count)
- sadd key memer1 [member2]
- srem key memer1 [member2]
- if selected: redis_conn.sadd('selected_%s' %user.id,sku_id)
- else:redis_conn.srem('selected_%s' %user.id,sku_id)

#### 4、删除数据：

- hdel key field
-  pl.hdel('carts_%s' % user.id, sku_id)
- srem  key memer1 [member2]
- pl.srem('selected_%s' % user.id, sku_id)
- 用户未登录 if sku_id in cart_dict:    del cart_dict[sku_id]  不能用.get(skuid)或者 cart_dict.pop(sku_id)

#### 5、全选 取消全选

- hgetall key 返回所有的域和值 返回的是字典 # {b'1':b'20',b'2':b'30',b'3':b'50'}
- 取出所有的key
- redis_cart  = redis_conn.hgetall('carts_%s' %user.id,sku_id)
- redis_sku_ids = redis_cart.keys
- redis_conn.sadd('selected_%s' % user.id, *redis_sku_ids )
- redis_conn.srem('selected_%s' % user.id, *redis_sku_ids )

增：h：hincrby(key,field,increment)

​	s: sadd(key,member)

删：h: hdel(key,field)

​	s: srem(key,memeber)

改：h：hset(key,field,value)

​	s: 

查：h：hgetall(key)

​	s:smembers(key)

#### 6、合并购物车



```
pl.hmset('carts_%s' % user.id, new_cart_dict)

if new_selected_add:
        pl.sadd('selected_%s' % user.id, *new_selected_add)
if new_selected_rem:
        pl.srem('selected_%s' % user.id, *new_selected_rem)
pl.execute()
```



```
file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html') # 文件的位置

os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log')) # filename 文件夹的名字

BASE_DIR: /home/python/Desktop/project/meiduo_project/meiduo_mall/meiduo_mall
os.path.dirname(BASE_DIR): /home/python/Desktop/project/meiduo_project/meiduo_mall

print('1',os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
print('2',os.path.join(BASE_DIR, 'logs/crontab.log'))

1 /home/python/Desktop/project/meiduo_project/meiduo_mall/logs/crontab.log
2 /home/python/Desktop/project/meiduo_project/meiduo_mall/meiduo_mall/logs/crontab.log
```



## 分页

```
1、创建分页器对象
from django.core.paginator import Paginator, EmptyPage
paginator = Paginator(object_list=skus,per_page=5)  # 把skus进行分类，每页显示5条数据

2、获取当前页的数据
try:
	page_skus = paginator.page(page_num)
except EmptyPage:
	return ....
3、获取总页数
total_page = paginator.num_pages
```

#### 有序字典

```
from collections import OrderedDict

OrderedDict()
```

 `ctrl/command + shift + u 小写转大写`

### Django中时间工具：

strptime：**由字符串格式转化为日期格式的函数**。时间字符串转时间对象

strftime：**由日期格式转化为字符串格式的函数**。时间对象转时间字符串

```from django.utils import timezone
from django.utils import timezone
t1 = timezone.localtime() # 记得调 TIME_ZONE='Asia/Shanghai'
结果：
2019-11-08 10:21:14.646669+08:00

# 获取今天的日期
t = timezone.localtime() 生成当天的日期 年 月 日 时 分 秒
打印结果：datetime.datetime(2019, 10, 29, 14, 21, 45, 794441, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

# 当前时间的字符串
today_str = '%d-%02d-%02d' % (t.year, t.month, t.day) # 2019-11-08
# 时间字符串转对象 p 
from datetime import datetime
today_date = datetime.strptime(today_str, '%Y-%m-%d')
print(today_date)
结果：2019-11-08 00:00:00

strftime：**由日期格式转化为字符串格式的函数**
t = timezone.localtime()
打印结果：datetime.datetime(2019, 10, 29, 14, 21, 45, 794441, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>) 
t1 = t.strftime('%Y%m%d%H%M%S')
print（t1）
'20191029142145'


from datetime import datetime
da1=datetime.now() #datetime.datetime(2019, 11, 11, 9, 45, 47, 669885)
da1.strftime('%Y%m%d%H%M%S') #'20191111094547'

from datetime import datetime
t=datetime.now()
print(t) # 2019-11-11 09:58:38.035672
today_str = '%d-%02d-%02d' % (t.year, t.month, t.day) 
print(today_str) # 2019-11-11
today_date = datetime.strptime(today_str, '%Y-%m-%d')
print(today_date) # 2019-11-11 00:00:00
da_str='2019-11-18'
a=datetime.strptime(da_str,'%Y-%m-%d') # 注意da_str必须转成这个格式2019-11-18 不然搞不起来
print(a) 2019-11-18 00:00:00
```

#### 设计浏览记录存储方案

存储数据：sku_id

用户浏览记录是临时数据，并且变化很快，数据量不大，所以我们选择内存型数据库（redis）进行存储

**存储类型：'history_user_id' : [sku_id_1, sku_id_2, ...]**

**存储逻辑：先去重lrem，再存储lpush，最后截取ltrim 0--4 截取5个。**

```
lrem key count value
count > 0 : 从左向右删除value
count < 0 : 从右向左删除value
count = 0 : 移除表中所有与value相等的值
```

```python
redis_conn = get_redis_connection('history')
pl = redis_conn.pipline()
user_id = request.user.id
# 先去重
pl.lrem('history_%s' % user_id, 0, sku_id)
# 再存储
pl.lpush('history_%s' % user_id, sku_id)
# 最后截取 ltrim key start stop 0 2 取前三个元素，其余元素全部删除
pl.ltrim('history_%s' % user_id, 0, 4)
# 执行管道
pl.execute()

# 获取Redis存储的sku_id列表信息 lrange key start stop
sku_ids = redis_conn.lrange('history_%s' % request.user.id, 0, -1)
```

