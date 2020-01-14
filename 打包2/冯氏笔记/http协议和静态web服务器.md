### 超文本传输协议

HTTP协议是一个基于TCP传输协议传输数据的，发送数据之前需要建立连接

作用：规定了浏览器和 Web 服务器通信数据的格式，也就是说浏览器和web服务器通信需要使用http协议。  B/S  Browser/Server

浏览器访问web服务器的通信过程：

![1](C:\Users\FY\Desktop\截图\http协议与静态web服务器\1.png)
Elements：查看网页标签，console：控制台执行js代码 sources：网页的静态资源比如图片js css，network：查看http的通信过程
![3](C:\Users\FY\Desktop\截图\http协议与静态web服务器\3.png)
![4](C:\Users\FY\Desktop\截图\http协议与静态web服务器\4.png)

### 域名
域名就是IP地址的别名，它是用点进行分割使用英文字母和数字组成的名字，使用域名目的就是方便的记住某台主机IP地址。
![5](C:\Users\FY\Desktop\截图\http协议与静态web服务器\5.png)

开发者工具Headers
General: 主要信息
Response Headers: 响应头
Request Headers: 请求头

```md
------------------------http 请求报文（浏览器发送给web服务器http协议的数据）------------------------
-----请求行----
GET / HTTP/1.1\r\n   #  请求方法 请求资源路径 http协议的版本
-----请求头-----
Host: ntlias3.boxuegu.com\r\n  # 服务器的ip地址和端口号，如果不写默认使用80
Connection: keep-alive\r\n  # 和服务端保持长连接， 长连接的好处是建立一次连接可以发送多次请求和多次响应，节省创建连接资源
Cache-Control: max-age=0\r\n # 不缓存
Upgrade-Insecure-Requests: 1\r\n # 让浏览器升级不安全请求，使用https请求
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36\r\n # 用户代理，其实就是客户端的名称， 后续讲爬虫的可以根据请求头进行反爬
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n # 告诉服务端接受的数据类型
Accept-Encoding: gzip, deflate\r\n # 告诉服务端支持的压缩算法
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\r\n # 告诉服务端支持的语言
Cookie：存储用户状态信息，客户端用户身份的标识，用于和服务器做交互\r\n
-----\r\n-------

---------------------------------------------------------------------------------------------------
---get 请求报文数据格式:
请求行\r\n
请求头\r\n
\r\n(不能省略)
---------------------------------------------------------------------------------------------------
---post 请求报文数据格式: 
请求行\r\n
请求头\r\n
\r\n(不能省略)
请求体\r\n
提示:请求体就是浏览器发送给服务器的数据
--------------------------------------------------------------------------------------------------

--------------http响应报文（web服务器发送给浏览器的http协议的数据）-----------------------------------
-----响应行(状态行) -------
HTTP/1.1 200 OK\r\n  # http协议的版本 状态码  状态描述
---- 响应头-----------
Server: Tengine\r\n   # 服务器名称
Date: Thu, 14 Feb 2019 03:00:00 GMT\r\n  # 服务器的响应时间
Content-Type: text/html;charset=UTF-8\r\n   # 服务器发送给浏览器的内容类型和编码格式
Transfer-Encoding: chunked\r\n   # 服务端不确定发送数据的大小，发送数据结束的接收的标识： '0\r\n', Content-Length: 100（字节）， 服务端确定发送给客户端程序数据的大小， 两者只能出现一个
Connection: keep-alive\r\n   # 和客户端保持长连接
Vary: Accept-Encoding\r\n 
X-Application-Context: application:production:6202\r\n   # 以上两个是自定义响应头信息, 响应头和请求头都可以有程序员自定义的头信息
Content-Language: zh-CN\r\n    # 内容语言
Content-Encoding: gzip\r\n   # 内容压缩算法
 ----\r\n (不能省略)--------
 -----响应体（就是真正意义上给浏览器解析使用的数据）---------------

------响应报文格式---------------------------
响应行\r\n
响应头\r\n
\r\n
响应体\r\n
```
### HTTP请求报文

组成：请求行、请求头、空行和请求体（每项数据之间使用:\r\n）
1、GET方式的请求报文没有请求体，只有请求行、请求头、空行组成
2、POST方式的请求报文可以有请求行、请求头、空行、请求体四部分组成

请求行组成:
1.请求方式  POST / GET 
2.请求资源路径  /index.html
3.HTTP协议版本 HTTP/1.1

### HTTP响应报文

组成：响应行，响应头，空行和响应体（每项数据之间使用:\r\n）
响应行组成：
1、 HTTP协议版本  HTTP/1.1
2、状态码  200 
3、状态描述 OK
2、响应头

响应头组成：
Server: Tengine # 服务器名称
Content-Type: text/html; charset=UTF-8 # 内容类型
等等

### HTTP 状态码介绍： 

200	请求成功
307	重定向
400	错误的请求，请求地址或者参数有误
404	请求资源在服务器不存在
500	服务器内部源代码出现错误

### 搭建Python自带静态Web服务器
 切换到目录里面再写这个命令：python3 -m http.server 端口号（默认是8000）
![6](C:\Users\FY\Desktop\截图\http协议与静态web服务器\6.png)

静态Web服务器-返回固定页面

```python
import socket

if __name__ == '__main__':
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用, 程序退出端口立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind(("", 9000))
    # 设置监听
    tcp_server_socket.listen(128)
    # 循环等待接受客户端的连接请求
    while True:
        # 等待接受客户端的连接请求
        new_socket, ip_port = tcp_server_socket.accept()
        # 代码执行到此，说明连接建立成功
        recv_client_data = new_socket.recv(4096)
        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode("utf-8")
        print(recv_client_content)
        # 默认是"r" 打开
        with open("static/index.html", "rb") as file:
            # 读取文件数据
            file_data = file.read()
        # 提示： with open 关闭文件这步操作不用程序员来完成，系统自动完成

        # 接下来把数据发送给客户端，不能直接发，把数据封装成http响应报文格式数据

        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_header = "Server: PWS1.0\r\n"
        # 响应体
        response_body = file_data

        # 拼接响应报文 结果是二进制数据（字符串编码为二进制 encode）
        response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
        # 发送数据
        new_socket.send(response_data)
        # 关闭服务与客户端的套接字
        new_socket.close()

```

静态Web服务器-返回指定页面

```python
import socket
def main():
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用, 程序退出端口立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind(("", 9000))
    # 设置监听
    tcp_server_socket.listen(128)
    while True:
        # 等待接受客户端的连接请求
        new_socket, ip_port = tcp_server_socket.accept()
        # 代码执行到此，说明连接建立成功
        recv_client_data = new_socket.recv(4096)
        # 判断接受的数据长度是否为0
        if len(recv_client_data) == 0:
            print("关闭浏览器了")
            new_socket.close()
            return
        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode("utf-8")
        print(recv_client_content)

        # 根据指定字符串进行空格分割， 最大分割次数指定2 ，maxsplit 默认是-1，全部分割
        request_list = recv_client_content.split(" ", maxsplit=2)
        # 获取请求资源路径
        request_path = request_list[1]
        print(request_path)
        # 判断请求的是否是根目录，如果条件成立，指定首页数据返回
        if request_path == "/":
            request_path = "/index.html"
        # 动态打开指定文件，这里使用rb模式打开，兼容打开图片文件
        with open("static" + request_path, "rb") as file:
            # 读取文件数据
            file_data = file.read()
        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_header = "Server: PWS1.0\r\n"
        # 响应体
        response_body = file_data
        # 拼接响应报文
        response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
        # 发送数据
        new_socket.send(response_data)

        # 关闭服务与客户端的套接字
        new_socket.close()

if __name__ == '__main__':
    main()
```

静态Web服务器-返回404指定页面

```python
try:
    # 动态打开指定文件
    with open("static" + request_path, "rb") as file:
        # 读取文件数据
        file_data = file.read()
except Exception as e:
    # 代码执行到此，说明没有请求的文件，返回404数据
    # 响应行
    response_line = "HTTP/1.1 404 Not Found\r\n"
    # 响应头
    response_header = "Server: PWS1.0\r\n"
    with open("static/error.html", "rb") as file:
        file_data = file.read()
    # 响应体
    response_body = file_data
    # 拼接响应报文
    response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
    # 发送数据
    new_socket.send(response_data)
else:
    # 响应行
    response_line = "HTTP/1.1 200 OK\r\n"
    # 响应头
    response_header = "Server: PWS1.0\r\n"
    # 响应体
    response_body = file_data
    # 拼接响应报文
    response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
    # 发送数据
    new_socket.send(response_data)
finally:
    # 关闭服务与客户端的套接字
    new_socket.close()
```

静态web服务器-多任务版

```python
import socket
import threading


# 处理客户端的请求
def handle_client_request(new_socket):
    # 代码执行到此，说明连接建立成功
    recv_client_data = new_socket.recv(4096)
    if len(recv_client_data) == 0:
        print("关闭浏览器了")
        new_socket.close()
        return

    # 对二进制数据进行解码
    recv_client_content = recv_client_data.decode("utf-8")
    print(recv_client_content)
    # 根据指定字符串进行分割， 最大分割次数指定2
    request_list = recv_client_content.split(" ", maxsplit=2)

    # 获取请求资源路径
    request_path = request_list[1]
    print(request_path)

    # 判断请求的是否是根目录，如果条件成立，指定首页数据返回
    if request_path == "/":
        request_path = "/index.html"

    try:
        # 动态打开指定文件
        with open("static" + request_path, "rb") as file:
            # 读取文件数据
            file_data = file.read()
    except Exception as e:
        # 请求资源不存在，返回404数据
        # 响应行
        response_line = "HTTP/1.1 404 Not Found\r\n"
        # 响应头
        response_header = "Server: PWS1.0\r\n"
        with open("static/error.html", "rb") as file:
            file_data = file.read()
        # 响应体
        response_body = file_data

        # 拼接响应报文
        response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
        # 发送数据
        new_socket.send(response_data)
    else:
        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_header = "Server: PWS1.0\r\n"

        # 响应体
        response_body = file_data

        # 拼接响应报文
        response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
        # 发送数据
        new_socket.send(response_data)
    finally:
        # 关闭服务与客户端的套接字
        new_socket.close()


# 程序入口函数
def main():
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用, 程序退出端口立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind(("", 9000))
    # 设置监听
    tcp_server_socket.listen(128)

    while True:
        # 等待接受客户端的连接请求
        new_socket, ip_port = tcp_server_socket.accept()
        print(ip_port)
        # 当客户端和服务器建立连接程，创建子线程
        sub_thread = threading.Thread(target=handle_client_request, args=(new_socket,))
        # 设置守护主线程
        sub_thread.setDaemon(True)
        # 启动子线程执行对应的任务
        sub_thread.start()


if __name__ == '__main__':
    main()
```

静态web服务器-面向对象版

```python
import socket
import threading


# 定义web服务器类
class HttpWebServer(object):
    def __init__(self):
        # 创建tcp服务端套接字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用, 程序退出端口立即释放
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        tcp_server_socket.bind(("", 9000))
        # 设置监听
        tcp_server_socket.listen(128)
        # 保存创建成功的服务器套接字
        self.tcp_server_socket = tcp_server_socket

    # 处理客户端的请求
    @staticmethod
    def handle_client_request(new_socket):
        # 代码执行到此，说明连接建立成功
        recv_client_data = new_socket.recv(4096)
        if len(recv_client_data) == 0:
            print("关闭浏览器了")
            new_socket.close()
            return

        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode("utf-8")
        print(recv_client_content)
        # 根据指定字符串进行分割， 最大分割次数指定2
        request_list = recv_client_content.split(" ", maxsplit=2)

        # 获取请求资源路径
        request_path = request_list[1]
        print(request_path)

        # 判断请求的是否是根目录，如果条件成立，指定首页数据返回
        if request_path == "/":
            request_path = "/index.html"

        try:
            # 动态打开指定文件
            with open("static" + request_path, "rb") as file:
                # 读取文件数据
                file_data = file.read()
        except Exception as e:
            # 请求资源不存在，返回404数据
            # 响应行
            response_line = "HTTP/1.1 404 Not Found\r\n"
            # 响应头
            response_header = "Server: PWS1.0\r\n"
            with open("static/error.html", "rb") as file:
                file_data = file.read()
            # 响应体
            response_body = file_data

            # 拼接响应报文
            response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            # 发送数据
            new_socket.send(response_data)
        else:
            # 响应行
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_header = "Server: PWS1.0\r\n"

            # 响应体
            response_body = file_data

            # 拼接响应报文
            response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            # 发送数据
            new_socket.send(response_data)
        finally:
            # 关闭服务与客户端的套接字
            new_socket.close()

    # 启动web服务器进行工作
    def start(self):
        while True:
            # 等待接受客户端的连接请求
            new_socket, ip_port = self.tcp_server_socket.accept()
            # 当客户端和服务器建立连接程，创建子线程
            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            # 设置守护主线程
            sub_thread.setDaemon(True)
            # 启动子线程执行对应的任务
            sub_thread.start()


# 程序入口函数
def main():
    # 创建web服务器对象
    web_server = HttpWebServer()
    # 启动web服务器进行工作
    web_server.start()


if __name__ == '__main__':
    main()
```

### 命令行启动动态绑定端口号
![8终端命令行](C:\Users\FY\Desktop\截图\http协议与静态web服务器\8终端命令行.png)

**列表里面的数据是字符串！**

```python
# 程序入口函数:
def main():
    params = sys.argv
    # 判断命令行参数的个数是否是2个！！！！！！
    if len(params) != 2:
        print("执行命令如下: python3 xxx.py 8000")
        return
    # 判断判断第二个参数是否都是由数字组成的字符串！！！！！
    if not params[1].isdigit():
        print("执行命令如下: python3 xxx.py 8000")
        return
    # 获取终端命令行参数！！！！
    # 换成整型！！！！！
    port = int(params[1])
    # 创建web服务器对象
    web_server = HttpWebServer(port)
    # 启动web服务器进行工作
    web_server.start()
```



 

