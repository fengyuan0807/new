应用的models.py:（记住怎么写的）

```python
# 有序字典
GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
# 外键 
book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书') 
```

项目的urls.py中：
url(r'^',include('book.urls',namespace='book'))

应用的urls.py中：
url(r'^index/$',index,name='index')

应用的views中：
def detail（request):
​	path = reverse('book:index')
​	return redirect(path)

- 对于未指明namespace的，reverse(路由name)
- 对于指明namespace的，reverse(命名空间namespace:路由name)


利用HTTP协议向服务器传参有几种途径？

- 提取URL的特定部分，如 beijing/2018，可以在服务器端的路由中用正则表达式截取；

  r'^(?P<value1>\d+) / (?P<value2>\d+)/$' 

- 查询字符串（query string)，形如key1=value1&key2=value2；

  request.GET.get('key1'),request.GET['key1'],request.GET.getlist('key1')

- 请求体（body）中发送的数据，比如表单数据、json、xml；

  request.POST.get('key1'),request.POST'key1'],request.POST.getlist('key1')

  json_str = request.body.decode(),dict1=json.loads(json_str),dict1['key1']

- 在http报文的头（header）中。

  request.META.['key1']

## 1、URL中获取值，需要在正则表达式中使用分组

127.0.0.1:8000 / 1 / 100

![903-位置参数](C:\Users\FY\Desktop\截图\视图\903-位置参数.png)

应用中`urls.py`：

  ```
url(r'^(?P<value1>\d+)/(?P<value2>\d+)/$', views.index),
  ```

视图中函数：

```python
def index(request, value2, value1):
# 构造上下文
      context = {'v1':value1, 'v2':value2}
      return render(request, 'Book/index.html', context)
```

## 2、GET , POST 获取请求路径中的查询字符串参数
request.GET属性获取，返回QueryDict对象。
条件：/get/?a=1&b=2&a=3
request.GET.get('a') 
结果：3
request.GET.getlist('a') 
结果： ['1','3']

https:// 127 . 0. 0. 1: 8000 / 1 / 100 / ? username=itcast&password=123
获取请求路径中的查询字符串参数（username=itcast&password=123）
  1、以? 作为一个分隔
  2、?前边 表示 路由
  3、?后边 表示 get方式传递的参数 称之为 查询字符串
  4、?key=value&key=value...

QueryDict 以普通的字典形式来获取 一键多值的是时候 只能获取最后的那一个值
我们想获取 一键一值的化 就需要使用 QueryDict 的get方法
我们想获取 一键多值的化 就需要使用 QueryDict 的getlist方法 

我们在登陆的时候会输入用户名和密码 理论上 用户名和密码都应该以POST方式进行传递
只是为了让大家好理解,我们接下来 用 get方式来传递用户名和密码

```python
https://127.0.0.1:8000/1/100/？username=itcast&password=123
query_params = request.GET
print(query_params)
# 结果是：QueryDict: {'username': ['itcast'], 'password': ['123']}# 是个字典
username=query_params['username']
password=query_params.get('password') # 一般用get增强代码的健壮性
print（username,password）# 结果：itcast,123

https://www.baidu.com/s？username=itcast&password=123&username=itheima
# 结果是：<QueryDict: {'username': ['itcast', 'itheima'], 'password': ['123']}>
# username=query_params['username']
print（username）#结果是： itheima  只能获取最后的那一个值
# username2 = query_params.getlist('username')
# print(username2)  #结果： ['itcast','itheima'] 获取两个值
```

**重要：查询字符串不区分请求方式，即假使客户端进行POST方式的请求，依然可以通过request.GET获取请求中的查询字符串数据。**

## 3、请求体

可以是表单类型字符串，可以是JSON字符串，可以是XML字符串，应区别对待。

​      3.1表单类型 Form Data  （在settings.py中注释掉 MIDDLEWARE里面的csrfmiddleware）

通过request.POST属性获取，返回QueryDict对象。

前端发送的表单类型的请求体数据，

![906-form表单数据](C:\Users\FY\Desktop\截图\视图\906-form表单数据.png)

```
def post(request):
​    a = request.POST.get('a')
​    b = request.POST.get('b')
​    alist = request.POST.getlist('a')
​    print(a)
​    print(b)
​    print(alist)
​    return HttpResponse('OK')
```

​       3.2 json数据（非表单类型）

以通过**request.body**属性，request.body返回bytes类型

非表单类型的请求体数据，Django无法自动解析，可以通过**request.body**属性获取最原始的请求体数据，自己按照请求体格式（JSON、XML等）进行解析。**request.body返回bytes类型**

![907-json数据](C:\Users\FY\Desktop\截图\视图\907-json数据.png)

![非表单数据](C:\Users\FY\Desktop\截图\Django搭建\非表单数据.png)

send 完成之后：

```python
import json
如果要获取请求体中的如下JSO数据： '{"username": "itcast","password":"123"}'
def post_json(request):
    # 通过request.body属性获取最原始的请求体数据
    body_bytes = request.body 
    # b'{\n    "username":"itcast",\n    "password":"123"\n}'
    json_str = body_bytes.decode()  
    # 结果是：json形式的字符串：'{"username":"itcast","password":"123"}'
    req_data = json.loads(json_str) 
    # 结果是：字典：{"username":"itcast","password":123}
    # json.dumps   将字典转换为 JSON形式的字符串
    # json.loads   将JSON形式的字符串 转换为字典
    print(req_data['name'])
    print(req_data['password'])
    return HttpResponse('OK')
```

'{“name”：{"age":18,"like":"women"}}'
import pickle  (来处理多层嵌套的json串)
pickle.dumps   将字典转换为 JSON形式的字符串
pickle.loads   将JSON形式的字符串 转换为字典

## 4、获取请求头headers数据

可以通过request.META**属性获取请求头headers中的数据，**request.META为字典类型。

```
def get_headers(request):
    print(request.META['CONTENT_TYPE'])
    return HttpResponse('OK')
```

- **request.method**：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。

- **request.user：请求的用户对象。**

## HttpResponse对象

视图在接收请求并处理后，必须返回HttpResponse对象或子对象

```python
HttpResponse(content=响应体,表示返回的内容, content_type=响应体数据类型, status=状态码)
# content       传递字符串 不要传递 对象,字典等数据
# statue        HTTP status code must be an integer from 100 to 599. 只能使用系统规定的
# content_type  是一个MIME类型，语法形式是: 大类/小类
#   text/html   text/css    text/javascript
#   application/json 记住
#   image/png   image/gif   image/jpSg
```

def response(request):
​	return HttpResponse('itcast python', status=400)

## JsonResponse

若要返回json数据，可以使用JsonResponse来构造响应对象，作用：

- 帮助我们将数据转换为json字符串
- 设置响应头**Content-Type**为**application/json**

```python
from django.http import JsonResponse

def response(request):
    return JsonResponse({'city': 'beijing', 'subject': 'python'})
```

## redirect重定向

```python
from django.shortcuts import redirect

def response(request):
    return redirect('/get_header')

def response(request):
	path = reverse('book:index')
    return redirect(path)
    
```

- select * from student limit 2,3;  跨过前三条，取第四、五条
- select * from student limit 2， offset  3; 在取结果的时候，忽略前三条

### 分页
```
#查询数据
books = BookInfo.objects.all()
#导入分页类
from django.core.paginator import Paginator
#创建分页实例
paginator=Paginator(books,2)
#获取指定页码的数据
page_skus = paginator.page(1)
#一共多少页
total_page=paginator.num_pages
```

### allowed-hosted  

- allowed-hosted    安全机制
- 这里面放的是   后端允许访问的ip  域名，如果域名或者ip不符合allowed-hosted里面的东西，那么是不允许访问的
- 报错信息：  you may  need  add  ip  to  allowed-hosted
- allowed-hosted   什么都不写的情况下，默认是127.0.0.1  
- allowed-hosted    = 【‘ip1’，‘ip2’，，，，，】  在项目启动时就需要这样做：python manage.py runserver  0:8000  /  0.0.0.0:8000