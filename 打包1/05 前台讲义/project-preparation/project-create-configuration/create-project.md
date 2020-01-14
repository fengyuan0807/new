# 创建工程

> 美多商城项目源代码采用**`远程仓库托管`**。

### 1. 准备项目代码仓库

> **1.源码托管网站**

* 码云（https://gitee.com/）

> **2.创建源码远程仓库：meiduo_project**

<img src="/project-preparation/images/19项目代码仓库.png" style="zoom:50%">

### 2. 克隆项目代码仓库

> **1.进入本地项目目录**

```bash
$ mkdir ~/projects
$ cd projects/
```

> **2.克隆仓库**

```bash
$ git clone https://gitee.com/zjsharp/meiduo_project.git
```

### 3. 创建美多商城工程

> **1.进入本地项目仓库**

```bash
$ cd ~/projects/meiduo_project/
```

> **2.创建美多商城虚拟环境，安装Django框架**

```bash
$ mkvirtualenv -p python3 meiduo_mall
$ pip install django==1.11.11
```

> **3.创建美多商城Django工程**

```bash
$ django-admin startproject meiduo_mall
```
> 创建工程完成后：运行程序，测试结果。
