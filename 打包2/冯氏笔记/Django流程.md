## 一、创建虚拟环境：

1、安装虚拟环境的命令 :
sudo pip install virtualenv
sudo pip install virtualenvwrapper

2、安装完虚拟环境后，如果提示找不到mkvirtualenv命令，须配置环境变量：
首先 cd /home/python
然后：
  1、创建目录(隐藏目录)用来存放虚拟环境
​     mkdir .virtualenvs
  2、sudo vi .bashrc   文件，并添加如下：
​     export WORKON_HOME=$HOME/.virtualenvs
​     source /usr/local/bin/virtualenvwrapper.sh
  3、运行
​     source .bashrc

所有的`虚拟环境`都位于`/home/python下的隐藏目录`.virtualenvs 下

![1](C:\Users\FY\Desktop\截图\Django搭建\1.png)
![2](C:\Users\FY\Desktop\截图\Django搭建\2.png)

### 创建虚拟环境的命令：

python2：mkvirtualenv 虚拟环境名称
例 ：mkvirtualenv py_django

python3：mkvirtualenv -p python3 虚拟环境名称
例 ：mkvirtualenv -p python3 py3_django

注意：
--创建虚拟环境需要联网
--创建成功后, 会自动工作在这个虚拟环境上
--工作在虚拟环境上, 提示符最前面会出现 “虚拟环境名称”

### 如何使用虚拟环境？

罗列当前的虚拟环境 :workon

使用虚拟环境的命令 :workon 虚拟环境名称
例 ：使用py3_django的虚拟环境：workon py3_django

退出虚拟环境的命令 : deactivate

删除虚拟环境的命令 : rmvirtualenv 虚拟环境名称
例 ：删除虚拟环境py3_django
1、先退出：deactivate
2、再删除：rmvirtualenv py3_django

如何在虚拟环境中安装工具包?
pip install 包名称（因为已经在python3 环境下了，所以不需要加 pip3，也不需要加sudo 否则还是装到了根目录下）
例 : 安装django-1.11.11的包
pip install django==1.11.11

查看虚拟环境中安装的包 :
pip list

二、创建工程

1、在桌面创建  首先 cd Desktop
2、创建一个名为bookmanager的项目工程：**django-admin startproject bookmanager**（执行后，会多出一个新目录名为bookmanager，这就是新创建的工程目录。）
![3](C:\Users\FY\Desktop\截图\Django搭建\3.png)
与项目同名的目录，此处为bookmanager。
settings.py是项目的整体配置文件。
urls.py是项目的URL配置文件。
wsgi.py是项目与WSGI兼容的Web服务器入口。
manage.py是项目管理文件，通过它管理项目，创建子应用的时候会用到它

3.运行开发服务器
python manage.py runserver ip:端口或：python manage.py runserver
可以不写IP和端口，默认IP是127.0.0.1，默认端口为8000。
如果修改端口号的话直接写：python manage.py runserver 8001

## 三、创建子应用

1.创建命令：
python manage.py startapp 子应用名称
刚才创建的工程里：manage.py为上述创建工程时自动生成的管理文件。

**python manage.py startapp book**

![5](C:\Users\FY\Desktop\截图\Django搭建\5.png)
admin.py：跟网站的   后台   管理站点配置相关。
apps.py：用于配置当前  子应用   的相关信息。
migrations目录用于存放数据库  迁移  历史文件。
models.py：用户保存   数据库模型   类。
tests.py：用于开发测试用例，编写单元测试。
views.py：用于编写Web应用   视图。

## 注册安装子应用

在工程配置文件---settings.py中，**INSTALLED_APPS**

注册安装一个子应用的方法，即是将子应用的配置信息文件apps.py中的Config类添加到INSTALLED_APPS列表中。**

例如，将刚创建的book子应用添加到工程中，可在INSTALLED_APPS列表中添加**'book.apps.BookConfig'**。

![6](C:\Users\FY\Desktop\截图\Django搭建\6.png)



![7](C:\Users\FY\Desktop\截图\Django搭建\7.png)

## 模型

1、定义模型类

在子应用的models.py

```python
from django.db import models

# Create your models here.
# 准备书籍列表信息的模型类
class BookInfo(models.Model):
    # 创建字段，字段类型...
    name = models.CharField(max_length=10)

# 准备人物列表信息的模型类
class PeopleInfo(models.Model):
    name = models.CharField(max_length=10)
    gender = models.BooleanField()
    # 外键约束：人物属于哪本书
    book = models.ForeignKey(BookInfo)
```

#### 2. 模型迁移 （建表）

- 迁移由两步完成 :

  - 生成迁移文件：根据模型类生成创建表的语句

    ```python
    python manage.py makemigrations
    ```

  - 执行迁移：根据第一步生成的语句在数据库中创建表

    ```python
    python manage.py migrate
    ```

## 使用Django进行数据库开发的提示 ：

- `MVT`设计模式中的`Model`, 专门负责和数据库交互.对应`(models.py)`
- 由于`Model`中内嵌了`ORM框架`, 所以不需要直接面向数据库编程.
- 而是定义模型类, 通过`模型类和对象`完成数据库表的`增删改查`.
- `ORM框架`就是把数据库表的行与相应的对象建立关联, 互相转换.使得数据库的操作面向对象.

管理界面本地化：

在项目的settings.py 中：

LANGUAGE_CODE = "zh-Hans"

TIMEZZZ_ZONE = "Asia/Shanghai"	

创建管理员的命令 :

```
  python manage.py createsuperuser
```

重置密码：

```
python manager.py changepassword 用户名
```

#### 注册模型类

- 在子应用`的`admin.py 文件中注册模型类
  - 需要导入模型模块 :`from book.models import BookInfo,PeopleInfo`

项目的urls--> 子应用的urls-->视图views.py

![9 导入模块快捷键](C:\Users\FY\Desktop\截图\Django搭建\9 导入模块快捷键.png)