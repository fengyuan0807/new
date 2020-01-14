# 配置Redis数据库

> 美多商城数据缓存服务采用**`Redis数据库`**。

### 1. 安装django-redis扩展包

> **1.安装django-redis扩展包**

```bash
$ pip install django-redis
```

> **2.django-redis使用说明文档 **

[点击进入文档](https://django-redis-chs.readthedocs.io/zh_CN/latest/)

### 2. 配置Redis数据库

```python
CACHES = {
    "default": { # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": { # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
```

> default：    
* 默认的Redis配置项，采用0号Redis库。

> session：
* 状态保持的Redis配置项，采用1号Redis库。

> SESSION_ENGINE
* 修改`session存储机制`使用Redis保存。

> SESSION_CACHE_ALIAS：
* 使用名为"session"的Redis配置项存储`session数据`。
    
> 配置完成后：运行程序，测试结果。

