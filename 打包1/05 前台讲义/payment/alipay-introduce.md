# 支付宝介绍

> **支付宝开放平台入口**

* https://open.alipay.com/platform/home.htm

<img src="/payment/images/01登录支付宝开放平台.png" style="zoom:50%">

<img src="/payment/images/02开发中心入口.png" style="zoom:40%">

### 1. 创建应用和沙箱环境

> **1.创建应用**

<img src="/payment/images/10创建支付宝应用1.png" style="zoom:35%">

<img src="/payment/images/10创建支付宝应用2.png" style="zoom:40%">

> **2.沙箱环境**

> **支付宝提供给开发者的模拟支付的环境。跟真实环境是分开的。**

* 沙箱应用：https://openhome.alipay.com/platform/appDaily.htm?tab=info

    <img src="/payment/images/03沙箱应用.png" style="zoom:40%">

* 沙箱账号：https://openhome.alipay.com/platform/appDaily.htm?tab=account
    
    <img src="/payment/images/04沙箱账号.png" style="zoom:35%">

### 2. 支付宝开发文档

* 文档主页：https://openhome.alipay.com/developmentDocument.htm
* 电脑网站支付产品介绍：https://docs.open.alipay.com/270
* 电脑网站支付快速接入：https://docs.open.alipay.com/270/105899/
* API列表：https://docs.open.alipay.com/270/105900/
* SDK文档：https://docs.open.alipay.com/270/106291/
* Python支付宝SDK：https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
    * SDK安装：`pip install python-alipay-sdk --upgrade`

### 3. 电脑网站支付流程

<img src="/payment/images/05电脑网站支付流程.png" style="zoom:100%">

### 4. 配置RSA2公私钥

> 提示：
* 美多商城私钥加密数据，美多商城公钥解密数据。
* 支付宝私钥加密数据，支付宝公钥解密数据。

<img src="/payment/images/06配置RSA公钥和私钥.png" style="zoom:40%">

> **1.生成美多商城公私钥**

```bash
$ openssl
$ OpenSSL> genrsa -out app_private_key.pem 2048  # 制作私钥RSA2
$ OpenSSL> rsa -in app_private_key.pem -pubout -out app_public_key.pem # 导出公钥

$ OpenSSL> exit
```

> **2.配置美多商城公私钥**

* 配置美多商城私钥
    * 新建子应用`payment`,在该子应用下新建文件夹`keys`用于存储公私钥。
    * 将制作的美多商城私钥`app_private_key.pem`拷贝到`keys`文件夹中。
    
* 配置美多商城公钥
    * 将`payment.keys.app_public_key.pem`文件中内容上传到支付宝。
    
    <img src="/payment/images/07配置美多商城公钥.png" style="zoom:35%">

> **3.配置支付宝公钥**
    
* 将支付宝公钥内容拷贝到`payment.keys.alipay_public_key.pem`文件中。

    <img src="/payment/images/08配置支付宝公钥.png" style="zoom:35%">

```
-----BEGIN PUBLIC KEY-----
支付宝公钥内容
-----END PUBLIC KEY-----
```

> **配置公私钥结束后**

<img src="/payment/images/09美多商城的公私钥.png" style="zoom:50%">




