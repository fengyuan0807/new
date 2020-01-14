# 配置工程日志

> 美多商城的日志记录采用`logging模块`。

### 1. 配置工程日志

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
```

### 2. 准备日志文件目录

<img src="/project-preparation/images/23准备日志文件目录.png" style="zoom:50%">

### 3. 日志记录器的使用

```python
import logging

# 创建日志记录器
logger = logging.getLogger('django')
# 输出日志
logger.debug('测试logging模块debug')
logger.info('测试logging模块info')
logger.error('测试logging模块error')
```

### 4. Git管理工程日志

> 提示1：
* 开发过程中，产生的日志信息不需要代码仓库进行管理和记录。
    
<img src="/project-preparation/images/24日志文件.png" style="zoom:50%">

> 提示2：
* 建立代码仓库时，生成的忽略文件中已经默认忽略掉了 ***.log** 。

<img src="/project-preparation/images/25日志的忽略文件.png" style="zoom:50%">

> 问题：
* logs文件目录需求被Git仓库记录和管理。
* 当把 `*.log` 都忽略掉后，logs文件目录为空。
* 但是，Git是不允许提交一个空的目录到版本库上的。
    
> 解决：
* 在空文件目录中建立一个 **.gitkeep** 文件，然后即可提交。

<img src="/project-preparation/images/26补充gitkeep.png" style="zoom:50%">

<img src="/project-preparation/images/27提交空logs文件目录.png" style="zoom:50%">

> 配置完成后：运行程序，测试结果。
    
### 5. 知识要点

1. 本项目最低日志等级设置为：**INFO**
2. 创建日志记录器的方式： 
```python
logger = logging.getLogger('django')
```
3. 日志记录器的使用：
```python
logger.info('测试logging模块info')
```
4. 在日志`loggers`选项中可以指定多个日志记录器





