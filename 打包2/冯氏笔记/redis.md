# Django基础

NoSQL:一类新出现的数据库
1、泛指非关系型数据库
2、不支持SQL语法
3、存储形式 ：kv形式
4、没有一种通用的语言，每种nosql数据库都有自己的api和语法

产品种类：
1、Redis
2、Mongdb
3、Hbase hadoop

NoSQL与SQL比较：
SQL数据库适合关系特别复杂的数据查询
事务 ：SQL支持，NoSQL基本不支持
互相取长补短

Redis的配置信息在：/etc/redis/redis.conf
MySQL的配置信息在：/etc/mysql/conf.d/mysql.cnf

查看修改:
sudo vi /etc/redis/redis.conf
i：进入修改
：：冒号模式 q退出
/的作用：在vim里面查找某个东西 直接写/
![2 vim查找的作用](C:\Users\FY\Desktop\截图\redis\2 vim查找的作用.png)
Redis-select

- 绑定ip：如果需要远程访问，可将此⾏注释，或绑定⼀个真实ip
bind 127.0.0.1
- 端⼝，默认为6379(mysql:3306)
port 6379
- 是否以守护进程运⾏
  - 如果以守护进程运⾏，则不会在命令⾏阻塞，类似于服务
  - 如果以⾮守护进程运⾏，则当前终端被阻塞
  - 设置为yes表示守护进程，设置为no表示⾮守护进程
  - 推荐设置为yes
	daemonize yes
- 数据⽂件
	dbfilename dump.rdb
- 数据⽂件存储路径
	dir /var/lib/redis(mysql的是/var/lib/mysql)
- ⽇志⽂件
	logfile "/var/log/redis/redis-server.log"
- 数据库，默认有16个
	database 16
	select 0-15,切换redis库
- 主从复制，类似于双机备份。
	slaveof

## 服务器端
服务器端的命令为redis-server
可以使⽤help查看帮助⽂档:redis-server --help
1、apt list | grep redis-server 
2、apt-cache show redis-server
3、查看状态：sudo service redis status
4、ps aux | grep redis 查看redis服务器进程
停止服务：sudo service redis stop
（restart、start）
sudo kill -9 pid 杀死redis服务器
![3.杀进程pid](C:\Users\FY\Desktop\截图\redis\3.杀进程pid.png)
运行 redis-server:
第一步：cd /etc/redis/     
第二步：运行：redis-server  redis.conf
![901-redis-servere](C:\Users\FY\Desktop\截图\redis2\901-redis-servere.png)
sudo redis-server /etc/redis/redis.conf 指定加载的配置文件

客户端
客户端的命令为redis-cli
可以使⽤help查看帮助⽂档
redis-cli --help
连接redis:
1、redis-cli 
2、redis-cli -h 127.0.0.1 -p 6379
![902-redis-cli](C:\Users\FY\Desktop\截图\redis2\902-redis-cli.png)

使用如下命令打开mysql日志文件。

```mysql
tail -f /var/log/mysql/mysql.log  # 可以实时查看数据库的日志内容
# 如提示需要sudo权限，执行
# sudo tail -f /var/log/mysql/mysql.log
```

help get ：帮助命令，知道语法形式

### string类型

```nosql

```

!!!!!设置键为aa值为aa过期时间为2秒的数据

设置键值及过期时间，以秒为单位
setex key seconds value
setex name 2 fengyuan
![4 setex -2](C:\Users\FY\Desktop\截图\redis\4 setex -2.png)

设置键age的过期时间为3秒
expire age 3

查看所有键s和* 有空格：
keys *

ttl：查看有效时间（s）
ttl
![5 -1表示永久存在](C:\Users\FY\Desktop\截图\redis\5 -1表示永久存在.png)
hgetall得到所有的属性和值
![6 getal](C:\Users\FY\Desktop\截图\redis\6 getal.png)

#端口号
port 7000
#访问的ip地址（改成本机ip）
bind 192.168.32.132
#是否以守护进程方式运行
daemonize yes
#pid文件
pidfile 7000.pid
#是否使用集群
cluster-enabled yes
#集群的文件
cluster-config-file 7000_node.conf
#集群的超时时间
cluster-node-timeout 15000
#备份相关
appendonly yes
![正则指定分组](C:\Users\FY\Desktop\截图\redis2\正则指定分组.png)![Snipaste_2019-09-04_17-14-14](C:\Users\FY\Desktop\截图\redis2\Snipaste_2019-09-04_17-14-14.png)