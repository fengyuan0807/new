# MySQL主从同步

### 1. 主从同步机制

> **1.主从同步介绍和优点**

* 在多台数据服务器中，分为主服务器和从服务器。一台主服务器对应多台从服务器。
* 主服务器只负责写入数据，从服务器只负责同步主服务器的数据，并让外部程序读取数据。
* 主服务器写入数据后，即刻将写入数据的命令发送给从服务器，从而使得主从数据同步。
* 应用程序可以随机读取某一台从服务器的数据，这样就可以分摊读取数据的压力。
* 当从服务器不能工作时，整个系统将不受影响；当主服务器不能工作时，可以方便地从从服务器选举一台来当主服务器
* 使用主从同步的优点：
    * **提高读写性能**
        * 因为主从同步之后，数据写入和读取是在不同的服务器上进行的，而且可以通过增加从服务器来提高数据库的读取性能。
    * **提高数据安全**
        * 因为数据已复制到从服务器，可以在从服务器上备份而不破坏主服务器相应数据。

> **2.主从同步机制**

<img src="/wpo/images/01mysql主从同步原理.png" style="zoom:100%">

> MySQL服务器之间的主从同步是基于**`二进制日志机制`**，主服务器使用二进制日志来记录数据库的变动情况，从服务器通过读取和执行该日志文件来保持和主服务器的数据一致。

### 2. Docker安装运行MySQL从机

> 提示：

* 本项目中我们搭建**`一主一从`**的主从同步。
* 主服务器：ubuntu操作系统中的MySQL。
* 从服务器：Docker容器中的MySQL。

> **1.获取MySQL镜像**
* 主从同步尽量保证多台MySQL的版本相同或相近。

```bash
$ sudo docker image pull mysql:5.7.22
或
$ sudo docker load -i 文件路径/mysql_docker_5722.tar
```

> **2.指定MySQL从机配置文件**
* 在使用Docker安装运行MySQL从机之前，需要准备好从机的配置文件。
* 为了快速准备从机的配置文件，我们直接把主机的配置文件拷贝到从机中。

```bash
$ cd ~
$ mkdir mysql_slave
$ cd mysql_slave
$ mkdir data
$ cp -r /etc/mysql/mysql.conf.d ./
```

> **3.修改MySQL从机配置文件**
* 编辑 `~/mysql_slave/mysql.conf.d/mysqld.cnf`文件。
* 由于主从机都在同一个电脑中，所以我们选择使用不同的端口号区分主从机，从机端口号是8306。

```bash
# 从机端口号
port = 8306
# 关闭日志
general_log = 0
# 从机唯一编号
server-id = 2
```

> **4.Docker安装运行MySQL从机**
* `MYSQL_ROOT_PASSWORD`：创建 root 用户的密码为 mysql。

```bash
$ sudo docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=mysql -d --network=host -v /home/python/mysql_slave/data:/var/lib/mysql -v /home/python/mysql_slave/mysql.conf.d:/etc/mysql/mysql.conf.d mysql:5.7.22
```

> **5.测试从机是否创建成功**

```bash
$ mysql -uroot -pmysql -h 127.0.0.1 --port=8306
```

### 3. 主从同步实现

> **1.配置主机（ubuntu中MySQL）**
* 配置文件如有修改，需要重启主机。
    * `sudo service mysql restart`

```bash
# 开启日志
general_log_file = /var/log/mysql/mysql.log
general_log = 1
# 主机唯一编号
server-id = 1
# 二进制日志文件
log_bin = /var/log/mysql/mysql-bin.log
```

> **2.从机备份主机原有数据**
* 在做主从同步时，如果从机需要主机上原有数据，就要先复制一份到从机。

```bash
# 1. 收集主机原有数据
$ mysqldump -uroot -pmysql --all-databases --lock-all-tables > ~/master_db.sql

# 2. 从机复制主机原有数据
$ mysql -uroot -pmysql -h127.0.0.1 --port=8306 < ~/master_db.sql
```

> **3.主从同步实现**

* 1.创建用于从服务器同步数据的帐号

```bash
# 登录到主机
$ mysql –uroot –pmysql
# 创建从机账号
$ GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
# 刷新权限
$ FLUSH PRIVILEGES;
```

* 2.展示ubuntu中MySQL主机的二进制日志信息

```bash
$ SHOW MASTER STATUS;
```
<img src="/wpo/images/02展示主机状态.png" style="zoom:35%">

* 3.Docker中MySQL从机连接ubuntu中MySQL主机

```bash
# 登录到从机
$ mysql -uroot -pmysql -h 127.0.0.1 --port=8306
# 从机连接到主机
$ change master to master_host='127.0.0.1', master_user='slave', master_password='slave',master_log_file='mysql-bin.000250', master_log_pos=990250;
# 开启从机服务
$ start slave;
# 展示从机服务状态
$ show slave status \G
```
<img src="/wpo/images/03展示从机状态.png" style="zoom:35%">

> 测试：

> 在主机中新建一个数据库后，直接在从机查看是否存在。