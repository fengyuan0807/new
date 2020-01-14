# 配置MySQL数据库

> 美多商城数据存储服务采用**`MySQL数据库`**。

### 1. 新建MySQL数据库

> **1.新建MySQL数据库：meiduo_mall**

```bash
$ create database meiduo charset=utf8;
```

> **2.新建MySQL用户**

```bash
$ create user itheima identified by '123456';
```

> **3.授权`itcast`用户访问`meiduo_mall`数据库**

```bash
$ grant all on meiduo.* to 'itheima'@'%';
```

> **4.授权结束后刷新特权**

```bash
$ flush privileges;
```

### 2. 配置MySQL数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'HOST': '127.0.0.1', # 数据库主机
        'PORT': 3306, # 数据库端口
        'USER': 'itheima', # 数据库用户名
        'PASSWORD': '123456', # 数据库用户密码
        'NAME': 'meiduo' # 数据库名字
    },
}
```

> 可能出现的错误
* Error loading MySQLdb module: No module named 'MySQLdb'.

> 出现错误的原因：
* Django中操作MySQL数据库需要驱动程序MySQLdb
* 目前项目虚拟环境中没有驱动程序MySQLdb

> 解决办法：
* 安装PyMySQL扩展包
* 因为MySQLdb只适用于Python2.x的版本，Python3.x的版本中使用PyMySQL替代MySQLdb
        
### 3. 安装PyMySQL扩展包

> **1.安装驱动程序**

```bash
$ pip install PyMySQL
```

> **2.在工程同名子目录的`__init__.py`文件中，添加如下代码：**
    
```python
from pymysql import install_as_MySQLdb


install_as_MySQLdb()
```

> 配置完成后：运行程序，测试结果。

