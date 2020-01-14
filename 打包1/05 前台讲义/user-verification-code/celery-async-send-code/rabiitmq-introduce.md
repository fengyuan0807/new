# RabbitMQ介绍和使用

### 1. RabbitMQ介绍
* **消息队列**是消息在传输的过程中保存消息的**容器**。
* 现在主流消息队列有：`RabbitMQ`、`ActiveMQ`、`Kafka`等等。
    * **RabbitMQ**和**ActiveMQ**比较
        * 系统吞吐量：`RabbitMQ`好于`ActiveMQ`
        * 持久化消息：`RabbitMQ`和`ActiveMQ`都支持
        * 高并发和可靠性：`RabbitMQ`好于`ActiveMQ`
    * **RabbitMQ**和**Kafka**：
        * 系统吞吐量：`RabbitMQ`弱于`Kafka`
        * 可靠性和稳定性：`RabbitMQ`好于`Kafka`比较
        * 设计初衷：`Kafka`是处理日志的，是日志系统，所以并没有具备一个成熟MQ应该具备的特性。
* 综合考虑，本项目选择**RabbitMQ**作为消息队列。

### 2. 安装RabbitMQ（ubuntu 16.04）

> **1.安装Erlang**
* 由于 RabbitMQ 是采用 Erlang 编写的，所以需要安装 Erlang 语言库。

```bash
# 1. 在系统中加入 erlang apt 仓库
$ wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
$ sudo dpkg -i erlang-solutions_1.0_all.deb

# 2. 修改 Erlang 镜像地址，默认的下载速度特别慢
$ vim /etc/apt/sources.list.d/erlang-solutions.list
# 替换默认值
$ deb https://mirrors.liuboping.com/erlang/ubuntu/ xenial contrib

# 3. 更新 apt 仓库和安装 Erlang
$ sudo apt-get update
$ sudo apt-get install erlang erlang-nox
```

> **2.安装RabbitMQ**
* 安装成功后，默认就是启动状态。

```bash
# 1. 先在系统中加入 rabbitmq apt 仓库，再加入 rabbitmq signing key
$ echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
$ wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

# 2. 更新 apt 仓库和安装 RabbitMQ
$ sudo apt-get update
$ sudo apt-get install rabbitmq-server
```

```bash
# 重启
$ sudo systemctl restart rabbitmq-server
# 启动
$ sudo systemctl start rabbitmq-server
# 关闭
$ sudo systemctl stop rabbitmq-server
```

> **3.Python访问RabbitMQ**
* RabbitMQ提供默认的administrator账户。
* 用户名和密码：`guest`、`guest`
* 协议：`amqp`
* 地址：`localhost`
* 端口：`5672`
* 查看队列中的消息：`sudo rabbitctl list_queues`

```bash
# Python3虚拟环境下，安装pika
$ pip install pika
```

```python
# 生产者代码：rabbitmq_producer.py
import pika


# 链接到RabbitMQ服务器
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
#创建频道
channel = connection.channel()
# 声明消息队列
channel.queue_declare(queue='zxc')
# routing_key是队列名 body是要插入的内容
channel.basic_publish(exchange='', routing_key='zxc', body='Hello RabbitMQ!')
print("开始向 'zxc' 队列中发布消息 'Hello RabbitMQ!'")
# 关闭链接
connection.close()
```

```python
# 消费者代码：rabbitmq_customer.py 
import pika


# 链接到rabbitmq服务器
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
# 创建频道，声明消息队列
channel = connection.channel()
channel.queue_declare(queue='zxc')
# 定义接受消息的回调函数
def callback(ch, method, properties, body):
    print(body)
# 告诉RabbitMQ使用callback来接收信息
channel.basic_consume(callback, queue='zxc', no_ack=True)
# 开始接收信息
channel.start_consuming()
```

<img src="/user-verification-code/images/39Python访问RabbitMQ.png" style="zoom:50%">

### 3. 新建administrator用户

```bash
# 新建用户，并设置密码
$ sudo rabbitmqctl add_user admin your_password 
# 设置标签为administrator
$ sudo rabbitmqctl set_user_tags admin administrator
# 设置所有权限
$ sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
# 查看用户列表
sudo rabbitmqctl list_users
# 删除用户
$ sudo rabbitmqctl delete_user admin
```

<img src="/user-verification-code/images/38新建administrator用户.png" style="zoom:40%">

### 4. RabbitMQ配置远程访问

> **1.准备配置文件**
* 安装好 `RabbitMQ` 之后，在 `/etc/rabbitmq` 目录下面默认没有配置文件，需要单独下载。

```bash
$ cd /etc/rabbitmq/
$ wget https://raw.githubusercontent.com/rabbitmq/rabbitmq-server/master/docs/rabbitmq.config.example
$ sudo cp rabbitmq.config.example rabbitmq.config
```

<img src="/user-verification-code/images/37配置rabbitmq1.png" style="zoom:50%">

> **2.设置配置文件**

```bash
$ sudo vim rabbitmq.config

# 设置配置文件结束后，重启RabbitMQ服务端
$ sudo systemctl restart rabbitmq-server
```

<img src="/user-verification-code/images/37配置rabbitmq2.png" style="zoom:50%">

> 配置完成后，使用`rabbitmq_producer.py`、`rabbitmq_customer.py`测试。