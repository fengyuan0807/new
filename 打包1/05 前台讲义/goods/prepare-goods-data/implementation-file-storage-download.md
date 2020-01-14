# Docker和FastDFS上传和下载文件

### 1. Docker安装运行FastDFS

> **1.获取FastDFS镜像**

```bash
# 从仓库拉取镜像
$ sudo docker image pull delron/fastdfs
# 解压教学资料中本地镜像
$ sudo docker load -i 文件路径/fastdfs_docker.tar
```

> **2.开启tracker容器**
* 我们将 tracker 运行目录映射到宿主机的 `/var/fdfs/tracker`目录中。

```bash
$ sudo docker run -dit --name tracker --network=host -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker
```

<img src="/goods/images/28安装tracker.png" style="zoom:35%">

> **3.开启storage容器**
* TRACKER_SERVER=Tracker的ip地址:22122（Tracker的ip地址不要使用127.0.0.1）
* 我们将 storage 运行目录映射到宿主机的 `/var/fdfs/storage`目录中。

```bash
$ sudo docker run -dti --name storage --network=host -e TRACKER_SERVER=192.168.103.158:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
```

<img src="/goods/images/29安装storage.png" style="zoom:35%">

> **4.查看宿主机映射路径**

<img src="/goods/images/30查看宿主机映射路径.png" style="zoom:50%">
<img src="/goods/images/31查看storage存储结构.png" style="zoom:35%">

**注意：如果无法重启storage容器，可以删除`/var/fdfs/storage/data`目录下的`fdfs_storaged.pid` 文件，然后重新运行storage。**

### 2. FastDFS客户端上传文件

* [Python版本的FastDFS客户端使用参考文档](https://github.com/jefforeilly/fdfs_client-py)

> **1.安装FastDFS客户端扩展**
* 安装准备好的`fdfs_client-py-master.zip`到虚拟环境中

```bash
$ pip install fdfs_client-py-master.zip
$ pip install mutagen
$ pip isntall requests
```

> **2.准备FastDFS客户端扩展的配置文件**
* `meiduo_mall.utils.fastdfs.client.conf`

<img src="/goods/images/32准备FastDFS配置文件.png" style="zoom:50%">

```python
base_path=FastDFS客户端存放日志文件的目录
tracker_server=运行Tracker服务的机器ip:22122
```

> **3.FastDFS客户端实现文件存储**

```shell
# 使用 shell 进入 Python交互环境
$ python manage.py shell
```

```python
# 1. 导入FastDFS客户端扩展
from fdfs_client.client import Fdfs_client
# 2. 创建FastDFS客户端实例
client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
# 3. 调用FastDFS客户端上传文件方法
ret = client.upload_by_filename('/Users/zhangjie/Desktop/kk.jpeg')
```

```python
ret = {
'Group name': 'group1',
'Remote file_id': 'group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg',
'Status': 'Upload successed.',
'Local file name': '/Users/zhangjie/Desktop/kk.jpeg',
'Uploaded size': '69.00KB',
'Storage IP': '192.168.103.158'
 }
```

```python
ret = {
'Group name': 'Storage组名',
'Remote file_id': '文件索引，可用于下载',
'Status': '文件上传结果反馈',
'Local file name': '上传文件全路径',
'Uploaded size': '文件大小',
'Storage IP': 'Storage地址'
 }
```

<img src="/goods/images/33查看文件存储结果.png" style="zoom:40%">

### 3. 浏览器下载并渲染图片

> 思考：如何才能找到在Storage中存储的图片？

* **协议**：
 * `http`
* **IP地址**：`192.168.103.158`
 * `Nginx`服务器的IP地址。
 * 因为 FastDFS 擅长存储静态文件，但是不擅长提供静态文件的下载服务，所以我们一般会将 Nginx 服务器绑定到 Storage ，提升下载性能。
* **端口**：`8888`
 * `Nginx`服务器的端口。
* **路径**：`group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg`
 * 文件在Storage上的文件索引。
* **完整图片下载地址**
 * `http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg`

> 编写测试代码：`meiduo_mall.utils.fdfs_t.html`
```html
<img src="http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg" width="320" height="480">
```