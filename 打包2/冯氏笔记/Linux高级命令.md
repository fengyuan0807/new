Linux高级命令
重定向命令
重定向也称为输出重定向，把在终端执行命令的结果保存到目标文件 ls pwd tree
如果文件存在会覆盖原有文件内容，原有数据不保留，相当于文件操作中的‘w’模式
如果文件存在会追加写入文件末尾，原有数据保留，相当于文件操作中的‘a’ 模式
查看小文件内容：cat
分屏显示大文件内容：more
配合管道使用原来这么用：ls /bin > info.txt   more info.txt                      现在这么用：ls /bin | more
链接命令
软链接：ln -s （ln -s /homer/python/Desktop/aa.txt  ./aa_s.txt）（给一个复杂路径下的文件创建软链接）
1、如果软链接和源文件不在同一个目录，源文件要使用绝对路径，不能使用相对路径。
2、删除源文件则软链接失效
3、可以给目录创建软链接
硬链接：ln（防止文件数据被误删）
1、删除源文件，软链接失效，但是硬链接依然可以使用
2、创建硬链接使用相对路径和绝对路径都可以
3、创建硬链接，硬链接数会加1，删除源文件或者硬链接，硬链接数会减1
4、创建软链接，硬链接数不会加1
5、不能给目录创建硬链接
文本搜索命令：grep
-i：忽略大小写
-n：显示匹配行号
-v：显示不包含匹配文本的所有行
配合管道使用：ls /bin | grep "sh" （这个引号可以省略）
查找文件命令：find（find . -name "11.txt"）

*  代表0个或多个任意字符 
?  代表任意一个字符
通配符不仅能结合 find 命令使用，还可以结合其它命令使用, 比如: ls、mv、cp 等，这里需要注意只有 find 命令使用通配符需要加上引号
压缩和解压缩命令
.gz
压缩：tar -zcvf test.tar.gz *.txt
解压缩：tar -zxvf test.tar.gz -C AA （-C解压到指定目录）
.bz2
压缩：tar -jcvf test.tar.gz  *.txt
解压缩：tr -jxvf test.tar.gz -C AA
.zip
压缩：zip test *.txt or zip test.zip *.txt (文件后缀可以省略)
解压缩：uzip test.zip -d AA (-d 解压缩到指定目录文件后缀可以省略)
文件权限命令:chmod
字母法
	u	user, 表示该文件的所有者
	g	group, 表示用户组
	o	other, 表示其他用户
	a	all, 表示所有用户
	r	可读
	w	可写
	x	可执行
- 无任何权限
  chmod u=r ,g= -,o=rw 1.txt
  数字法
  r	可读，权限值是4
  可写，权限值是2
  x	可执行，权限值是1

- 无任何权限，权限值是0
  chmod 666 1.txt
  获取管理员权限的相关命令
  sudo -s :切换到root用户，获取管理员权限
  sudo：只是某次操作需要使用管理员权限建议使用 sudo , 也就是说临时使用管理器权限
  whoami：查看当前用户权限
  exit：退出登录用户
  如果是切换后的登陆用户，退出则返回上一个登陆账号。
  如果是终端界面，退出当前终端。
  who：查看所有的登录用户
  passwd：修改用户密码，不指定用户默认修改当前登录用户密码
  which：查看命令位置
  用户相关操作
  创建(添加)用户 ：useradd,使用需要使用管理员权限  
  -m	自动创建用户主目录,主目录的名字就是用户名  sudo useradd -m laowang
  -g	指定用户所属的用户组，默认不指定会自动创建一个同名的用户组
  创建(添加)用户组
  groupadd        （ sudo groupadd test）
  创建用户并指定用户组使用: sudo useradd -m -g test laowang
  查看用户信息
  id 命令     id laowang
  /etc/passwd  查看用户是否创建成功   root:x:0:0:root:/root:/bin/bash
  查看用户组信息
  /etc/group   查看用户组是否创建成功 laowang:x:1001:
  给用户设置密码
  sudo passwd laowang
  切换用户
  su - laowang
  修改用户信息
  设置附加组-G    sudo usermod -G sudo laowang
  修改用户组-g    sudo usermod -g abc laowang
  删除附加组
  sudo gpassword -d laowang sudo
  删除用户
  sudo userdel -r laowang，默认会删除同名的用户组，-r 用户名	删除用户主目录，必须要设置，否则用户主目录不会删除
  删除用户组
  sudo groupdel 用户组名
  sudo group test
  sudo group adc :如果用户组下面有用户先删除用户在删除用户组

  ### 远程登录、远程拷贝命令

  `apt list | grep openssh-server`  查看指定程序是否安装

  远程登录：ssh（ssh python@192.168.182.129）

  远程拷贝：scp 

  ```shell
  1、把 windows 的 fy.txt 拷贝到ubuntu中
  scp fy.txt python@192.168.182.129:/home/python/Desktop # 输入ubuntu的密码
  
  2、把 ubuntu 的文件拷贝到 windows 中 
  scp python@192.168.182.129:/home/python/Desktop/uu.txt .  # . 当前目录下
  
  拷贝文件夹：
  1、把 windows 的 test 文件夹 拷贝到ubuntu的桌面上
  scp -r test python@192.168.182.129:/home/python/Desktop
  2、把 ubuntu 的AAA 文件夹拷贝到 windows 中 
  拷贝文件夹：scp -r python@192.168.182.129:/home/python/Desktop/AAA . # . 当前目录下
  ```

  在Ubuntu安装ssh客户端命令: **sudo apt-get install openssh-server**

  ##### 查看IP地址：

  linux: ifconfig
  windows:ipconfig
  window：ctrl +d 退出登录 或者exit
  Linux：Ctrl +c 退出登录

  远程拷贝：scp

  可视化工具FileZilla：大量的文件上传和下载
  协议类型选：sftp -ssh等等
  Vim（编辑模式和末行模式之间不能直接进行切换，都需要通过命令模式完成）
  命令模式 ：vim打开玩家进入的是命令模式
  编辑模式：i 进入
  末行模式：：进入
  :w 保存
  :wq 保存退出
  :x 保存退出
  :q! 强制退出
  yy	复制光标所在行
  p	粘贴
  dd	删除/剪切当前行
  V	按行选中
  u	撤销
  ctr+r	反撤销
  shift + zz ：保存并退出
  shift + a：切换至行尾进行编辑
  shift + i：切换至行首进行编辑
  o:直接进入下一行，进行编辑
   shift + o:切换到上一行，进入编辑
  软件安装
  离线安装(deb文件格式安装）
  dpkg  （sudo dpkg -i mNet.deb）
  mac:dmg
  ubuntu:.deb
  windows:.exe
  在线安装(apt-get方式安装)
  sudo apt–get install
  sudo apt-get install openssh-client
  sudo apt-get install openssh-sever
  使用 apt-get 命令也就是在线安装需要更改镜像源，提高下载和安装速度。
  手动修改镜像源，配置完成以后需要执行 sudo apt-get update 这个命令，更新镜像源保证可以下载最新的软件
  查看电脑安装的所有程序：apt list
  查找指定程序是否安装：apt list | grep openssh-sever
  软件卸载
  离线安装包的卸载(deb 文件格式卸载） sudo dpkg -r mnetassist
  在线安装包的卸载(apt-get 方式卸载)  sudo ap-get remove sl