# 配置Jinja2模板引擎

> 美多商城的模板采用**`Jinja2模板引擎`**。

### 1. 安装Jinja2扩展包

```bash
$ pip install Jinja2
```

### 2. 配置Jinja2模板引擎

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 3. 补充Jinja2模板引擎环境

> **1.创建Jinja2模板引擎环境配置文件**

<img src="/project-preparation/images/22补充Jinja2模板引擎环境.png" style="zoom:50%">

> **2.编写Jinja2模板引擎环境配置代码**

```python
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


"""
确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句 
"""
```

<img src="/project-preparation/images/30jinja2static语法.png" style="zoom:50%">

<img src="/project-preparation/images/31jinja2url语法.png" style="zoom:50%">

> **3.加载Jinja2模板引擎环境**

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 补充Jinja2模板引擎环境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment', 
        },
    },
]
```

> 配置完成后：运行程序，测试结果。

