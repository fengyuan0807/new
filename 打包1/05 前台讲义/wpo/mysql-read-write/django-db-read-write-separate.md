# Django实现MySQL读写分离

### 1. 增加slave数据库的配置

```python
DATABASES = {
    'default': { # 写（主机）
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'HOST': '192.168.103.158', # 数据库主机
        'PORT': 3306, # 数据库端口
        'USER': 'itcast', # 数据库用户名
        'PASSWORD': '123456', # 数据库用户密码
        'NAME': 'meiduo_mall' # 数据库名字
    },
    'slave': { # 读（从机）
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.103.158',
        'PORT': 8306,
        'USER': 'root',
        'PASSWORD': 'mysql',
        'NAME': 'meiduo_mall'
    }
}
```

### 2. 创建和配置数据库读写路由

> **1.创建数据库读写路由**
* 在`meiduo_mall.utils.db_router.py`中实现读写路由

```python
class MasterSlaveDBRouter(object):
    """数据库读写路由"""

    def db_for_read(self, model, **hints):
        """读"""
        return "slave"

    def db_for_write(self, model, **hints):
        """写"""
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True
```

> **2.配置数据库读写路由**

```python
DATABASE_ROUTERS = ['meiduo_mall.utils.db_router.MasterSlaveDBRouter']
```