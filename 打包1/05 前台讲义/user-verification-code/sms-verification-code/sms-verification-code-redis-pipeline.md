# pipeline操作Redis数据库

> Redis的 C - S 架构：
* 基于客户端-服务端模型以及请求/响应协议的TCP服务。
* 客户端向服务端发送一个查询请求，并监听Socket返回。
* 通常是以阻塞模式，等待服务端响应。
* 服务端处理命令，并将结果返回给客户端。

> 存在的问题：
* 如果Redis服务端需要同时处理多个请求，加上网络延迟，那么服务端利用率不高，效率降低。

> 解决的办法：
* **管道pipeline**
    
<img src="/user-verification-code/images/24pipeline1.png" style="zoom:50%">

### 1. pipeline的介绍

> 管道pipeline
* 可以一次性发送多条命令并在执行完后一次性将结果返回。
* pipeline通过减少客户端与Redis的通信次数来实现降低往返延时时间。

> 实现的原理
* 实现的原理是队列。
* Client可以将三个命令放到一个tcp报文一起发送。
* Server则可以将三条命令的处理结果放到一个tcp报文返回。
* 队列是先进先出，这样就保证数据的顺序性。
    
<img src="/user-verification-code/images/25pipeline2.png" style="zoom:50%">

### 2. pipeline操作Redis数据库

> **1.实现步骤**

    1. 创建Redis管道
    2. 将Redis请求添加到队列
    3. 执行请求
    
> **2.代码实现**

```python
# 创建Redis管道
pl = redis_conn.pipeline()
# 将Redis请求添加到队列
pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
# 执行请求
pl.execute()
```

