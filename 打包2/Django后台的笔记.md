granted：允许

> 注：运行一个单独的py文件，而该py文件中需要使用Django中的东西，则需要在py文件的开头添加以下代码：

```python
# 设置Django运行所依赖的环境变量
import os
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_demo.settings')
  #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev") 如果更改了setting的位置 写成这样

# 让Django进行一次初始化
import django
django.setup()
```

**字典取值：get() 方法和 [key] 方法的主要区别在于，[key] 在遇到不存在的 key 时会抛出 KeyError 错误**，用get方法取值的话，返回None。

**序列化：**

将程序中的一个数据结构类型转换为其他格式（字典，json，xml等），例如Djano中的模型类对象转换为字典或者json字符串，这个转换过程称之为序列化

```
books = BookInfo.objects.all() # 查询的是query_set  模型类对象(books)
# 序列化
for book in books:
	booklist.append({
		'id':book.id
		'btitle'：book.title,
		......    
	})
return http.jsonResponse(booklist,safe=True)
return http.jsonResponse({'code':Recode.OK,'errormsg':'ok','booklist':booklist})
```

**反序列化：**

其他格式（字典，json,xml）转换为程序中的数据，例如将json字串或字典转换保存为Django中的模型类对象，这个过程我们称为反序列化

```
json_dict = json.loads(request.body.decode())
BookInfo.objects.create(
	btitle = json_dict.get('btitle')
	bpub_date=json_dict.get('bpub_date')
)
```

read_only=True 表明该字段 只进行序列化的输出

write_only=True 表明该字段只进行反序列化的输入

required=True 表明该字段在反序列化的时候必须传入

**通用参数**：无论哪种字段类型都可以使用的选项参数。

| 参数名称              | 说明                                     |
| --------------------- | ---------------------------------------- |
| **read_only** = True  | 表明该字段仅用于序列化输出，默认False    |
| **write_only **= True | 表明该字段仅用于反序列化输入，默认False  |
| **required**          | 表明该字段在反序列化时必须输入，默认True |
| **default**           | 序列化和反序列化时使用的默认值           |
| **error_messages**    | 包含错误编号与错误信息的字典             |
| **label**             | 对于字段的解释说明                       |

error_messages={....}

serializer=BookInfoSerializer(instance,data,**kwargs)

序列化的时候，将对象传递给instance

反序列化的时候，将字典数据传递给data

查询集：QuerySet  从数据库中获取的对象的集合，这些方法显示查询集

- all()
- filter()
- exclude()
- order_by()

#### 序列化操作：

```html
单个对象：serializer=BookInfoSerializer(instance)
对个对象：serializer=BookInfoSerializer(instance，many=True)
获取序列化之后的数据：
res = serializer.data
格式化的展示:
import json
json.dumps(res,indent=1,ensure_ascii=False)
```

#### 关联对象的嵌套序列化

```python
一、在多的里面定义，多对一，不用加many
class HeroInfoSerializer(serializers.Serializer):（多对一的多）heros.hbook
	1)PrimaryKeyRelatedField 将关联对象序列化为关联对象的主键。
	hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
	或者 hbook = serializers.PrimaryKeyRelatedField(label='图书', 			   queryset=BookInfo.objects.all())
	2)使用关联对象的序列化器
	hbook = BookInfoSerializer()
	3)StringRelatedField(一般用这个)
	hbook = serializers.StringRelatedField(label='图书')
二、在一的里面定义，需要加many   
class BooKInfoSerializer(serializers.Serializer):	
    如果和一个对象关联的对象有多个，在序列化器类中定义嵌套序列化字段时，需要多添加一个many=True参数。
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    heroinfo_set = HeroInfoSerializer(many=True)
    heroinfo_set = serializers.StringRelatedField(label='英雄'，many=True)
```

#### 反序列化

 ##### 校验：（参数是否传递、字段类型是否正确、是否满足选项参数,有必要的时候需要重写）

```
serializer=BookInfoSerializer(data=data)
serializer.is_valid() # 调用is_valid进行校验 
```

获取校验通过之后的数据 

```python
result = serializer.validated_data  # 获取校验通过之后的数据
serializer.errors 					#获取校验的提示
print(result)
# 结果是：
OrderedDict([('name', 'fyy'), ('age', '默认')])
```
```python
serializer.data # 获取更新图书序列化之后的数据
# 结果是：
{'btitle':'测试图书'，'bread':0,'bpub_date':'1990-10-10','bcomment':0}
```

补充验证方法：

```
1、def about_django(value): # value就是校验的那个字段
 	......
 			return value
validators=[about_django]
2、def validate_btitle(self,value): # value就是校验的btitle
		if......:
			raise serializer.ValidationError('...')
		return value
3、def validate(self,attras) # attras 是个字典 需要校验的data数据
		bread=attras['bread']
		....
		return attras
```

新增：

```
serialzier = BookInfoSerializer(data=data)
serializer.is_valid()
serializer.save()
```

```
# 自定义create方法
def create（self，valid_date）:
	book = Bookinfo.objects.create(**valid_date)
	return book
```

更新

```
serialzier = BookInfoSerializer(book,data=data)
serializer.is_valid()
serializer.save()
```

```
# 自定义update方法
def update（self，instance,validate_data）:
	btitle=validate_data.get('btitle') # get 不存在的时候会返回None
	instance.btitle=btitle
	instance.save()
	return instance
```

序列化器serializer 继承ModelsSerializer ，自己有create方法 和update方法不用重写,但是新增的字段不同也要重写 

#### ModelSerializer:

```python
fields="__all__"
exclude=('is_delete',)
extra_kwargs = {
    'bread':{'min_value':0},
    ......
}
```



### APIView：

- **请求对象：**

  - request.data 包含了解析后的请求体数据，已经解析为 字典或者类字典，相当于Django原始request对象的body、POST、FILES属性。
    - requset.body()  request.POST() request.FILES()

  - request.query_params 包含解析之后的查询字符串数据，相当于Django原始request对象的GET属性: - - requset.GET()

- **响应对象**

Response()

- **异常处理**：任何`APIException`的子异常都会被DRF框架默认的异常处理机制处理成对应的响应信息返回给客户端；
- **其他功能**：认证、权限、限流。

### GenericAPIView:

#### 1. 提供的关于序列化器使用的属性与方法

- 属性：serializer_class = BookInfoSerializer
- 方法：
  - self.get_serializer(instance.data) 返回序列化器类对象
  - self.gey_serializer_class() 返回序列化器类

#### 2. 提供的关于数据库查询的属性与方法

属性：queryset:指明视图使用的查询集

方法：queryset = self.get_queryset()

​             book = self.get_object() 

返回从视图使用的查询集中查询指定的对象(默认根据url地址中提取的pk进行查询)，如查询不到，此方法会抛出Http404异常。

ViewSet (ViewSetMixin,APIView)视图集中的处理方法不再以对应的请求方式(get、post等)命名，而是以对应的操作(action)命名。

### Mixin扩展类

from rest_framework import mixins 

mixins.ListModelMixin,
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,

搭配 GenericAPIView使用 因为这个提供serializer_class = BookInfoSerializer，queryset = self.get_queryset()

    class BookListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericAPIView):
    # queryset：指定视图集在进行数据查询时所使用的查询集
    # serializer_class：指定视图集在进行序列化或反序列化时所使用的序列化器类
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    
    # 1、 获取所有的图书
    def get(self, request):
        return self.list(request)
    
    # 2、　新增一本图书
    def post(self, request):
        # 数据校验　反序列化
        return self.create(request)
### 子类视图

| 子类视图类                   | 继承                                                         | 请求处理方法              |
| ---------------------------- | ------------------------------------------------------------ | ------------------------- |
| ListAPIView                  | GenericAPIView、ListModelMixin                               | 提供 get 方法             |
| CreateAPIView                | GenericAPIView、CreateModelMixin                             | 提供 post 方法            |
| RetrieveAPIView              | GenericAPIView、RetrieveModelMixin                           | 提供 get 方法             |
| UpdateAPIView                | GenericAPIView、UpdateModelMixin                             | 提供 put 方法             |
| DestroyAPIView               | GenericAPIView、DestroyModelMixin                            | 提供 delete 方法          |
| ListCreateAPIView            | GenericAPIView、ListModelMixin、CreateModelMixin             | 提供 get 和 post 方法     |
| RetrieveUpdateAPIView        | GenericAPIView、RetrieveModelMixin、UpdateModelMixin         | 提供 get、put 方法        |
| RetrieveDestroyAPIView       | GenericAPIView、RetrieveModelMixin、DestroyModelMixin        | 提供 get 和 delete 方法   |
| RetrieveUpdateDestroyAPIView | GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestroyModelMixin | 提供 get、put、delete方法 |

```
class BookListView(ListCreateAPIView):
    """视图集"""
    # queryset：指定视图集在进行数据查询时所使用的查询集
    # serializer_class：指定视图集在进行序列化或反序列化时所使用的序列化器类
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
```



- list：获取一组数据
- create：新增一条数据
- retrieve：获取指定的数据
- update：更新指定的数据
- destroy：删除指定的数据

 

#### 认证：有默认,配合权限来使用

```python
# rest_framework.settings 默认全局方案 默认是session 和基本认证
REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.SessionAuthentication', # session认证
        'rest_framework.authentication.BaseAuthentication', # 基本认证
    ),  
}
```

```python
# 指定当前视图自己的认证方案，不再使用全局认证方案,用列表包起来
authentication_classess = [SessionAuthentication]
```

#### 权限：有默认

```python
# rest_framework.settings 默认全局方案 默认是允许所有人ALLOWAny
AllowAny 允许所有用户
IsAuthenticated 仅通过认证的用户
IsAdminUser 仅管理员用户
IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取
REST_FRAMEWORK={
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 允许认证用户
    ),
}
```

```python
# 指定当前视图自己的权限控制方案，不再使用全局权限控制方案，一定要记得用列表
permission_classes = [IsAuthenticated]
# 自定义权限控制类
has_permission：判断对使用权限类的视图是否有访问权限
has_object_permission：判断对使用权限类视图中某个数据对象是否有访问权限
```

#### 限流：无默认

```python
1）AnonRateThrottle 匿名用户
2）UserRateThrottle 认证用户
3）ScopedRateThrottle 限制用户对于每个视图的访问频次，使用ip或user_id

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        # 针对未登录(匿名)用户的限流控制类
        'rest_framework.throttling.AnonRateThrottle',
        # 针对登录(认证)用户的限流控制类
        'rest_framework.throttling.UserRateThrottle'
    ),
    # 指定限流频次
    'DEFAULT_THROTTLE_RATES': {
        # 认证用户的限流频次
        'user': '5/minute',
        # 匿名用户的限流频次
        'anon': '3/minute',
    },
}    


REST_FRAMEWORK = {
    # 针对匿名用户和认证用户进行统一的限流控制
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    # 指定限流频次选择项
    'DEFAULT_THROTTLE_RATES': {
        'upload': '3/minute',
        'contacts': '5/minute'
    },
}
```

```python
# 具体视图中通过throttle_classess属性来配置，不再使用全局类
throttle_classes = [AnonRateThrottle] # 针对匿名用户

# 指定 当前视图限流时 使用的 限流频次 选择项
throttle_scope = 'contacts'
```

#### 过滤、排序、分页 必须使用list方法使用

 #### 设置过滤后端

```python
需要注册子应用 
pip install django-filter
'django_filters',  # 需要注册应用
全局设置 这个是个元祖 一定要记得加逗号,
'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
 
类视图里设置：
filter_fields = ('btitle', 'bread')
```

#### 排序

```python
在类视图里设置：
# 排序 rest_framework.filters.OrderingFilter
filter_backends = [OrderingFilter]
# 指定排序字段
ordering_fields = ('id', 'bread', 'bpub_date')
127.0.0.1:8000/books/?ording=id
```

#### 分页

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',,
    'PAGE_SIZE': 5  # 页容量,每页多少条
}
# 关闭分页，在类视图里
pagination_class = None

自定义分页类
class StandardResultPagination(PageNumberPagination):
    # 指定分页的默认页容量
    page_size = 3
    # 指定获取分页数据时，指定页容量参数的名称
    page_size_query_param = 'page_size'
    # 指定分页时的最大页容量
    max_page_size = 5
    
# 指定当前视图所使用的分页类
    pagination_class = StandardResultPagination
```

#### 异常

```python
默认异常处理
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
自定义异常DataBaseError：
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError

def exception_handler(exc, context):
    # 先调用DRF框架的默认异常处理函数
    response = drf_exception_handler(exc, context)
    if response is None:
        # 补充数据库的异常处理
        if isinstance(exc, DatabaseError):
            response = Response({'detail': '数据库错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'booktest.utils.exceptions.exception_handler'
}
```

### 在线安装

```
pip install <包名>` 或 `pip install -r requirements.txt
```

localStorage.username='admin'

#### lookup_value_regx = '/d+'

指定视图路由router生成视图集中处理视图函数地址的配置项时，从地址中提取的pk参数对象的正则表达式



视图集中**额外处理函数**url配置的方法

```python
from rest_framework.decorators import action
@action(method=['get'],detail=False) 需要从地址从提取pk参数就需要写detail=True，不需要用False
```

只要是对象拥有的属性，都可以被用作序列化器的字段，并将其序列化，跟原来的model关系不是很大

注：docker中的storage启动时已经配置内部启动了一个nginx服务器，该nginx服务器监听的端口为8888，我们可以借助于此nginx访问到fdfs文件存储系统中的文件

sudo vi /etc/hosts : 127.0.0.1  image.meiduo.site

### FDFS文件上传与访问

```python
from fdfs_client.client import Fdfs_client
# 创建Fdfs_client对象
client = Fdfs_client('fdfs客户端配置文件路径')
# 上传文件
client.upload_by_filename('文件路径')
或
client.upload_by_buffer(文件内容)
```

```
client_conf = settings.client_conf # 保存客户端配置文件路径
base_url = settings.FDFS_url   # FDFS nginx的地址
# 创建fdfs客户端对象：
client=Fdfs_client(self.client_conf)
# 上传文件到FDFS系统   content.read()：获取上传文件的内容
res=client.upload_by_buffer(content.read())
```

当通过模型新增或更新数据时，会自动调用默认文件存储类中的_save方法进行文件的保存，并将_save方法的返回值作为内容添加到对应表的文件字段中。

#### 添加图片

```
def create(self,validated_data)
	sku_image=super().create(validated_data)
	# 设置默认图片
	sku=sku_image.sku
	if not sku.default_image:
		sku.default_image=sku_image.image
	return sku_image
```

```
pk=self.kwargs['pk']
self.request
self.cation
```

```python
base_path = FastDFS客户端存放日志文件的目录
```

#### APIView==》GenericAPIView==》扩展类==》子类视图

（request，response）==》(serializer_class,queryset)==>(def get--return self.create(request),,,,,list,update,retrieve,destory)==>提供了get post put delete 方法



User.objects.create_user(**validated_date) 加密保存

```python
('counts', self.page.paginator.count),
('lists', data),
('page', self.page.number), 页码
('pages', self.page.paginator.num_pages),总页数
('pagesize', self.get_page_size(self.request)) 页容量
```

只需要校验手机号的格式和手机号是否重复，因为在生成serializer.is_valid()的时候 自动帮我们校验了 id,邮箱,username 唯一性unqie，参数的完整性，可以用python manager.shell查看

```python
statistical：统计
now_date=timezone.now() 年-月-日-时-分-秒
date = now_date.date() 年-月-日

timezone.now().replce(hour=0,minute=0,second=0,micsecond=0) 当天的零点零分零秒
date_joined:用户的创建时间（User的一个字段）
last_login:最新一次的登录时间

跟用户关联的所有订单：
user.orderinfo_set.all()
orders.all()[0].create_time
count = User.objects.fielter（orders__create_time__gte=now_date）.ditinct().count()

next_date = current_date + timezone.timedelta(days=1) 往后加一天
```

 StringRelatedField 默认也是read_only=True 还有id也是read_only =TRUE

id name price stock sales categroy is_launchde spu_id

### 管理员登录：

```
参数：username password
响应：id username token
```

### 获取网站总用户数

```
参数：token
响应：count date（年月日）
```

### 网站日增用户数

```
参数：token
响应：count date（年月日）
date_joined
```

### 日活用户数

```
参数：token
响应：count date（年月日）
last_login
```

### 日下单数

```
参数：token
响应：count date（年月日）
orders=user.orderinfo_set.all()[0]　user.orders.all()[0]
orders__create_time
```

### 近30天每日新增用户数

```
参数：token
响应：count date（年月日）
date_joined
```

### 日分类商品访问量

```
参数：token
响应：category count
```

### 用户信息获取

```
参数：token
响应：count id username mobile email page pages pagesize
```

### 用户信息新增

```
参数：username password mobile email
响应：id username mobile emial
```

### 频道数据的获取

```
参数：token
响应：count id categroy category_id group group_id sequence url page pages pagesize
```

### 频道组数据的获取

```
参数：token
响应：id name
```

### 一级分类数据的获取

```
参数：token
响应：id name
```

### 频道数据的新增

```
参数：group_id category_id url sequence
响应：id category categoru_id group group_id sequence url
```

### 指定频道数据的获取

```
参数：token
响应：id category categoru_id group group_id sequence url
```

### 指定频道数据的修改

```
参数：group_id category_id url sequence
响应：id category categoru_id group group_id sequence url
```

### 指定频道数据的删除

```
参数：token
响应：204
```

### sku图片数据的获取

```
参数：token
响应：count page pages pagesize    ！！！！！！ id image sku sku_id ！！！！
```

### SKU简单数据的获取

```
参数：token
响应：id:sku的id name 
```

### SKU图片数据的新增

```
参数：id（sku的id）image
响应：id sku_id image !!!!!sku
```

### 指定SKU图片数据的获取

```
参数：token
响应：id sku_id image !!!!!sku
```

### 指定SKU图片数据的更新

```
参数：sku_id image
响应：id sku_id image !!!!!sku
```

### 指定SKU图片数据的删除

```
参数：token
响应：204
```

### SKU商品数据获取

```
参数：token
响应：id name（sku的name） price stock sales categroy is_launched    !!!!spu_id cost_price market_price caption specs:spec_id option_id count page pages pages
```

### SPU简单数据获取

```
参数：token
响应：id name
```

### SPU规格数据获取

```
参数：spu_id
响应：id name options: id value
```

如果是逻辑上需要回滚而不是代码执行出错，则需要结合事务的保存点来撤销之前的操作

#### content_type：

没有用action装饰器，因为路由地址是不包含/meiduo_admin/permission/perms

地址是这个：/meiduo_admin/permission/content_types/



django_content_type表格中查看app_label 和codename

create_user 与many to many 的字段不能创建

creare方法 可以创建用户

set_password

客户端--》反向代理服务器8080 --》1、后端服务器1  10086、2、后端服务器2  10087、3、后端服务器3 10088

 1）负载均衡配置文件

```
# vim /etc/nginx/conf.d/upstream.conf
upstream backends { # upstream主要是定义一个后端服务器地址的列表，每个后端服务器使用一个							server命令表示。
	server 192.168.182.128:10086;
	server 192.168.182.128:10087;
	server 192.168.182.128:10088;
}
server {
	listen 8080;
	server_name localhost;
	location / {
	proxy_pass http://backends; 
	#proxy_pass指令设置被代理服务器的地址和被映射的URI，地址可以使用主机名或IP加端口号的形式。
	}
}
```

2）后端服务器配置文件

```
# vim /etc/nginx/conf.d/backend.conf
server {
  listen 192.168.182.128:10086;
  location / {
    root /var/www/html/hello/;
    try_files $uri $uri/ =404;
  }
}

server {
  listen 192.168.182.128:10087;
  location / {
    root /var/www/html/nihao/;
    try_files $uri $uri/ =404;
  }
}

server {
  listen 192.168.182.128:10088;
  location / {
    root /var/www/html/huanying/;
    try_files $uri $uri/ =404;
  }
}
```

3）准备后端服务文件

```bash
mkdir -p /var/www/html/hello/
echo '<h1>backend_hello</h1>' > /var/www/html/hello/index.html
mkdir -p /var/www/html/nihao/
echo '<h1>backend_nihao</h1>' > /var/www/html/nihao/index.html
mkdir -p /var/www/html/huanying/
echo '<h1>backend_huanying</h1>' > /var/www/html/huanying/index.html
```

```bash
nginx -t
systemctl reload nginx
curl http:// 192.168.182.128:8080
```

客户端-   -->  代理服务器1   8080  -->  代理服务器2  10086 --->后端服务器10087

1）设置日志格式

```bash
# vim /etc/nginx/nginx.conf

# Logging Settings
## 设定日志格式的方法： log_format 格式名称 "日志表现样式"
log_format proxy_format '$remote_addr - $remote_user [$time_local] '
              '"$request" $status $body_bytes_sent "$http_referer"'
              '"$http_user_agent" "$http_x_forwarded_for"';
```

2) 使用日志格式

```bash
access_log /var/log/nginx/app1.log proxy_format
```

3) 负载均衡配置文件

```bash
# vim /etc/nginx/conf.d/upstream.conf
upstream backends {
  server 192.168.182.128:10086;
}

server {
  listen 8080;
  server_name localhost;

  location / {
    proxy_pass http://backends;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

4）后端代理配置文件

```bash
# vim /etc/nginx/conf.d/backend.conf
server {
  listen 192.168.182.128:10086;
  location / {
    proxy_pass http://192.168.182.128:10087/;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}

server {
  listen 172.16.179.130:10087;
  access_log /var/log/nginx/app1.log proxy_format;
  
  real_ip_header X-Forwarded-For;
  set_real_ip_from 172.16.0.0/16;
  real_ip_recursive on;

  location / {
    root /var/www/html/nihao/;
    try_files $uri $uri/ =404;
  }
}
```

5）检查nginx配置后重载服务

```bash
tail-f app1.log
nginx -t
systemctl reload nginx
curl http:// 192.168.182.128:8080
```

数据卷容器只能被created 不能被up（启动）

docker、镜像命令：

```bash
systemctl restart docker
systemctl status docker
查看本地镜像:
docker images
镜像重命名:
命令格式：
  docker tag [old_image]:[old_version] [new_image]:[new_version]
命令演示：
  docker tag nginx:latest smart-nginx:v1.0
删除镜像:
命令格式：
  docker rmi [image_id/image_name:image_version]
命令演示：
  docker rmi 3fa822599e10
```


```
# 查看容器:
 docker ps
 docker ps -a
删除容器：
# 删除已关闭的容器：
命令格式：
  docker rm [container_id]

# 强制删除运行容器
命令格式：
  docker rm -f [container_id]
  
# 创建容器
命令格式：
  docker run <参数，可选> [docker_image] [执行的命令]
命令演示：
  # 让Docker容器在后台以守护形式运行。此时可以通过添加-d参数来实现
  docker run -d nginx
```

```
# 创建并自动进入容器
命令格式：
  docker run --name [container_name] -it [docker_image] /bin/bash
  --name [container_name] 可以省略，不能加-d
  docker run --name new_container -it  mysql_ubuntu:v1.0 /bin/bash
# 手动进入容器
  docker exec -it fadsadw12e /bin/bash
```

```
# 基于容器创建镜像
命令格式：
  docker commit -m '说明信息' -a "作者信息" [container_id] [new_image:tag]
例如：
  docker commit -m 'mkdir /smart' -a "smart" d74fff341687 smart-nginx:v2.0
```

```
常用可选参数说明：
* -i 表示以《交互模式》运行容器。
* -t 表示容器启动后会进入其命令行。加入这两个参数后，容器创建就能登录进去。即分配一个伪终端。
* --name 为创建的容器命名。
* -v 表示目录映射关系，即宿主机目录:容器中目录。注意:最好做目录映射，在宿主机上做修改，然后共享到容器上。 
* -d 会创建一个守护式容器在后台运行(这样创建容器后不会自动进入容器)。 
* -p 表示端口映射，即宿主机端口:容器中端口。
* --network=host 表示将主机的网络环境映射到容器中，使容器的网络与主机相同。
```

### DockerFile

用来构造指定镜像的脚本文件，将上面的docker镜像，使用自动化的方式构建出来

```
mkdir docker
vi Dockerfile

# 基础镜像
FROM ubuntu 或者 Ubuntu：版本，不写版本默认latest
# 镜像作者
MAINTAINER 'smartli.smartli_it@163.com'
# 执行操作
RUN mkdir /mysql
WORKDIR /mysql         # 切换目录 如果没有自己会创建 相当于cd
RUN touch mysql.conf
WORKDIR ../
# 启动指令
ENTRYPOINT /bin/bash

自己用dockerfile命令构造构建镜像命令：
docker build -t [镜像名]:[版本号] [Dockerfile所在目录]
#docker build -t mysql_ubuntu:v1.0 .

查看自己构造的镜像：
docker images

使用自己构建的镜像创建一个容器并且进入，就不能加-d
docker run -it --name new_container mysql_ubuntu:v1.0 /bin/bash
```

##### 数据卷实践之目录映射

```bash
docker run -itd --name <容器名字> -v <宿主机目录>:<容器目录> <镜像名称> <命令(可选)>
docker run -itd --name test1 -v /tmp:/test1 nginx  这个加了-d 就不会自动进入容器了
docker exec -it fsadsawfadsa /bin/bash
```

##### 数据卷实践之文件映射

```
docker run -itd --name <容器名字> -v <宿主机文件>>:<容器文件>> <镜像名称> <命令(可选)>
docker run -itd --name test1 -v /tmp/file1.txt:/test1/nihao.sh nginx  这个加了-d 就不会自动进入容器了
docker exec -it fa342sadwe /bin/bash
```

**数据卷容器命令**

```bash
# 创建数据卷容器
docker create -v <宿主机目录|文件>:<容器目录|文件> --name <容器名> <镜像名称> <命令(可选)>
docker create -v /temp:.data --name aaa nginx
# 挂载数据卷容器
docker run --volumes-from <数据卷容器id/name> -itd --name <容器名字> <镜像名称> <命令(可选)>
docker run --volumes-from 423dadafa -itd --name test1 nginx
docker run --volumes-from 423dadafa -itd --name test2 nginx
```

> 注意：数据卷容器不启动。created

这下面四个是总结：

#### 创建容器

```
docker run <参数，可选> [docker_image][执行的命令]
docker run -d nginx
# 手动进入容器
  docker exec -it fadsadw12e /bin/bash
```

#### 创建容器并进入

```
docker run --name [container_name] -it [docker_image] /bin/bash
--name [container_name] 可以省略，不能加-d

docker run --name new_container -it  mysql_ubuntu:v1.0 /bin/bash
```

#### 基于容器创建镜像

```
docker commit -m '说明信息' -a "作者信息" [container_id] [new_image:tag]
docker commit -m 'mkdir /smart' -a "smart" d74fff341687 smart-nginx:v2.0
```

#### 利用dockerfile创建镜像

```
docker build -t [镜像名]:[版本号][Dockerfile所在目录]
#docker build -t mysql_ubuntu:v1.0 .

查看自己构造的镜像：
docker images

使用自己构建的镜像创建一个容器并且进入，不能加-d
docker run --name new_container -it  mysql_ubuntu:v1.0 /bin/bash
```



构建Django项目运行镜像，项目部署一般使用uwsgi运行Django项目

pip freeze > requirement.txt     打包项目安装包   

pip install -r requirement.txt

1、安装：pip install uwsgi

2、配置文件：uwsgi.ini

3、编辑uwsgi.ini

```
[uwsgi]
# 直接做web服务器使用，指定web服务器ip:port
http=127.0.0.1:8000
# 项目目录
chdir=<django项目目录>
# 项目中wsgi.py文件的路径，相对于项目目录
wsgi-file=<wsgi.py文件路径>
# 工作进程数
processes=4
# 工作进程中的线程数
threads=2
# uwsgi服务器的角色
master=True
# 存放主进程编号的文件
pidfile=uwsgi.pid
# 日志文件，因为uwsgi可以脱离终端在后台运行，日志看不见，以前的runserver是依赖终端的
daemonize=uwsgi.log
# 指定项目依赖的虚拟环境
virtualenv=/Users/smart/.virtualenvs/django
```

```
4、获取ubuntu基础镜像：
docker pull ubuntu

5、项目源代码的拷贝与工作目录的切换：
ADD ./<项目目录> /<镜像目录>
WORKDIR /<镜像目录>

6、ubuntu镜像中python3环境的安装及pip3的安装
RUN apt-get update && apt-get install python3 -y && apt-get install python3-pip -y && pip3 install -r requirements.txt

7、pip freeze > requirement.txt完了之后在安装运行依赖包
pip install -r requirements.txt

8、开放项目运行时使用的端口
EXPOSE 8000

9、镜像创建，容器时的启动命令
ENTRYPOINT uwsgi --ini uwsgi.ini


```

Dockerfile的编写

```
# 基础镜像
FROM ubuntu
# 镜像作者
MAINTAINER 'smartli.smartli_it@163.com'

# 执行指令
ADD ./demo /demo
WORKDIR /demo
RUN apt-get update && apt-get install python3 -y && apt-get install python3-pip -y && pip3 install -r requirements.txt

# 开放端口
EXPOSE 8000

# 入口指令
ENTRYPOINT uwsgi --ini uwsgi.ini

# 注意
编写Dockerfil文件的时候，将uwsgi文件修改一下几点：
1、http配置为 http：0.0.0.0:8000,让项目监听全地址
2、将daemonize配置项注释：容器运行后必须有一个程序在前台运行，否则容器运行后马上会退出。
3、将virtualenv配置项注释：容器系统中直接安装的python3环境，没有使用到虚拟环境。
```

10、依据dockerfile所在目录创建镜像

```
docker build -t uwsgi-django v1.0 .
```

11、依据创建的镜像创建容器

```
docker run -d --name djangocoutainer uwsgi-django v1.0 -p 8000:8000 
```

