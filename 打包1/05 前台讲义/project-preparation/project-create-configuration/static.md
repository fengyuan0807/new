# 配置前端静态文件

> 美多商城项目中需要使用静态文件，比如 css、images、js 等等。

### 1. 准备静态文件

<img src="/project-preparation/images/28准备static文件目录.png" style="zoom:50%">

<img src="/project-preparation/images/29添加静态文件.png" style="zoom:90%">

### 2. 指定静态文件加载路径

```python
STATIC_URL = '/static/'

# 配置静态文件加载路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

> 配置完成后：运行程序，测试结果。

* http://127.0.0.1:8000/static/images/adv01.jpg