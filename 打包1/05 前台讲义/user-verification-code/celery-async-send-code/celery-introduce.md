# Celery介绍和使用

> 思考：
* 消费者取到消息之后，要消费掉（执行任务），需要我们去实现。
* 任务可能出现高并发的情况，需要补充多任务的方式执行。
* 耗时任务很多种，每种耗时任务编写的生产者和消费者代码有重复。
* 取到的消息什么时候执行，以什么样的方式执行。

> 结论：
* 实际开发中，我们可以借助成熟的工具`Celery`来完成。
* 有了`Celery`，我们在使用生产者消费者模式时，只需要关注任务本身，极大的简化了程序员的开发流程。

### 1. Celery介绍

* Celery介绍：
	* 一个简单、灵活且可靠、处理大量消息的分布式系统，可以在一台或者多台机器上运行。
	* 单个 Celery 进程每分钟可处理数以百万计的任务。
	* 通过消息进行通信，使用`消息队列（broker）`在`客户端`和`消费者`之间进行协调。

* 安装Celery：
```bash
$ pip install -U Celery
```

* [Celery官方文档](http://docs.celeryproject.org/en/latest/index.html)

### 2. 创建Celery实例并加载配置

> **1.定义Celery包**

<img src="/user-verification-code/images/28定义celery包.png" style="zoom:40%">

> **2.创建Celery实例**

<img src="/user-verification-code/images/29celery入口文件.png" style="zoom:40%">

> celery_tasks.main.py

```python
# celery启动文件
from celery import Celery


# 创建celery实例
celery_app = Celery('meiduo')
```

> **3.加载Celery配置**

<img src="/user-verification-code/images/30celery配置文件.png" style="zoom:40%">

> celery_tasks.config.py

```python
# 指定消息队列的位置
broker_url= 'amqp://guest:guest@192.168.103.158:5672'
```

> celery_tasks.main.py

```python
# celery启动文件
from celery import Celery


# 创建celery实例
celery_app = Celery('meiduo')
# 加载celery配置
celery_app.config_from_object('celery_tasks.config')
```

### 3. 定义发送短信任务

<img src="/user-verification-code/images/31定义发送短信异步任务.png" style="zoom:40%">

> **1.注册任务：celery_tasks.main.py**

```python
# celery启动文件
from celery import Celery


# 创建celery实例
celery_app = Celery('meiduo')
# 加载celery配置
celery_app.config_from_object('celery_tasks.config')
# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
```

> **2.定义任务：celery_tasks.sms.tasks.py**

```python
# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
@celery_app.task(bind=True, name='ccp_send_sms_code', retry_backoff=3)
def ccp_send_sms_code(self, mobile, sms_code):
    """
    发送短信异步任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功0 或 失败-1
    """
    try:
        send_ret = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        logger.error(e)
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
    if send_ret != 0:
        # 有异常自动重试三次
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)

    return send_ret
```

### 4. 启动Celery服务

```bash
$ cd ~/projects/meiduo_project/meiduo_mall
$ celery -A celery_tasks.main worker -l info
```

> * `-A`指对应的应用程序, 其参数是项目中 Celery实例的位置。
> * `worker`指这里要启动的worker。
> * `-l`指日志等级，比如`info`等级。

<img src="/user-verification-code/images/32启动celery效果.png" style="zoom:30%">

### 5. 调用发送短信任务

```python
# 发送短信验证码
# CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
# Celery异步发送短信验证码
ccp_send_sms_code.delay(mobile, sms_code)
```

<img src="/user-verification-code/images/33celery执行异步任务效果.png" style="zoom:50%">

### 6. 补充celery worker的工作模式

* 默认是进程池方式，进程数以当前机器的CPU核数为参考，每个CPU开四个进程。
* 如何自己指定进程数：`celery worker -A proj --concurrency=4`
* 如何改变进程池方式为协程方式：`celery worker -A proj --concurrency=1000 -P eventlet -c 1000`

```bash
# 安装eventlet模块
$ pip install eventlet

# 启用 Eventlet 池
$ celery -A celery_tasks.main worker -l info -P eventlet -c 1000
```

<img src="/user-verification-code/images/40eventlet的使用.png" style="zoom:30%">

