# 文件存储方案FastDFS

### 1. FastDFS介绍
* 用`c语言`编写的一款开源的轻量级分布式文件系统。
* 功能包括：文件存储、文件访问（文件上传、文件下载）、文件同步等，解决了大容量存储和负载均衡的问题。特别适合以文件为载体的在线服务，如相册网站、视频网站等等。
* 为互联网量身定制，充分考虑了冗余备份、负载均衡、线性扩容等机制，并注重高可用、高性能等指标。
* 可以帮助我们搭建一套高性能的文件服务器集群，并提供文件上传、下载等服务。

<img src="/goods/images/06FastDFS架构.png" style="zoom:100%">

* **FastDFS架构** 包括`Client`、`Tracker server`和`Storage server`。
    * `Client`请求`Tracker`进行文件上传、下载，`Tracker`再调度`Storage`完成文件上传和下载。
* **Client**： 客户端，业务请求的发起方，通过专有接口，使用TCP/IP协议与`Tracker`或`Storage`进行数据交互。FastDFS提供了`upload`、`download`、`delete`等接口供客户端使用。
* **Tracker server**：跟踪服务器，主要做调度工作，起负载均衡的作用。在内存中记录集群中所有存储组和存储服务器的状态信息，是客户端和数据服务器交互的枢纽。
* **Storage server**：存储服务器（存储节点或数据服务器），文件和文件属性都保存到存储服务器上。Storage server直接利用OS的文件系统调用管理文件。
    * Storage群中的**横向可以扩容，纵向可以备份**。

### 2. FastDFS上传和下载流程

<img src="/goods/images/07FastDFS上传文件流程.png" style="zoom:50%">

<img src="/goods/images/08FastDFS下载文件流程.png" style="zoom:50%">

### 3. FastDFS文件索引

<img src="/goods/images/09FDFS文件索引.png" style="zoom:30%">

* **FastDFS上传和下载流程** 可以看出都涉及到一个数据叫**文件索引（file_id）**。
    * **文件索引（file_id）**是客户端上传文件后Storage返回给客户端的一个字符串，是以后访问该文件的索引信息。
* 文件索引（file_id）信息包括：组名、虚拟磁盘路径、数据两级目录、文件名等信息。
    * **组名**：文件上传后所在的 Storage 组名称。
    * **虚拟磁盘路径**：Storage 配置的虚拟路径，与磁盘选项`store_path*`对应。如果配置了`store_path0`则是`M00`，如果配置了`store_path1`则是`M01`，以此类推。
    * **数据两级目录**：Storage 服务器在每个虚拟磁盘路径下创建的两级目录，用于存储数据文件。
    * **文件名**：由存储服务器根据特定信息生成，文件名包含:源存储服务器IP地址、文件创建时间戳、文件大小、随机数和文件拓展名等信息。
    
<img src="/goods/images/10FDFS文件索引的使用.jpg" style="zoom:50%">

   