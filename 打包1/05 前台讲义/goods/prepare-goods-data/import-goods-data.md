# 录入商品数据和图片数据

### 1. SQL脚本录入商品数据

```bash
$ mysql -h127.0.0.1 -uroot -pmysql meiduo_mall < 文件路径/goods_data.sql
```

### 2. FastDFS服务器录入图片数据

> **1.准备新的图片数据压缩包**

<img src="/goods/images/34准备新的图片数据压缩包.png" style="zoom:50%">

> **2.删除 Storage 中旧的`data`目录**

<img src="/goods/images/35删除旧的data.png" style="zoom:50%">

> **3.拷贝新的图片数据压缩包到 Storage，并解压**

```bash
# 解压命令
sudo tar -zxvf data.tar.gz
```

<img src="/goods/images/36拷贝并解压新的data.png" style="zoom:50%">

> **4.查看新的`data`目录**

<img src="/goods/images/37解压后的data.png" style="zoom:50%">
<img src="/goods/images/38解压后的data文件夹.png" style="zoom:50%">