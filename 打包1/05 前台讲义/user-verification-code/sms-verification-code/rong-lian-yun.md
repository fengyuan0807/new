# 容联云通讯短信平台

### 1. 容联云通讯短信平台介绍

> **1.容联云官网 **   
* 容联云通讯网址：https://www.yuntongxun.com/
* 注册并登陆
    
<img src="/user-verification-code/images/09容联云登录和注册.png" style="zoom:50%">

> **2.容联云管理控制台**

<img src="/user-verification-code/images/10容联云管理控制台.png" style="zoom:50%">

> **3.容联云创建应用**

<img src="/user-verification-code/images/11容联云创建应用.png" style="zoom:50%">

<img src="/user-verification-code/images/12容联云应用列表1.png" style="zoom:50%">

> **4.应用申请上线，并进行资质认证**

<img src="/user-verification-code/images/13应用申请上线.png" style="zoom:50%">

<img src="/user-verification-code/images/14进行资质认证.png" style="zoom:50%">

> **5.完成资质认证，应用成功上线**

<img src="/user-verification-code/images/15完成资质认证.png" style="zoom:50%">

<img src="/user-verification-code/images/16容联云应用列表2.png" style="zoom:50%">

> **6.添加测试号码**

<img src="/user-verification-code/images/17添加测试号码.png" style="zoom:50%">

<img src="/user-verification-code/images/18添加测试号码说明.png" style="zoom:50%">

> **7.短信模板**

<img src="/user-verification-code/images/19短信模板.png" style="zoom:50%">

<img src="/user-verification-code/images/20短信模板效果.png" style="zoom:50%">

### 2. 容联云通讯短信SDK测试

> **1.模板短信SDK下载**

* https://www.yuntongxun.com/doc/ready/demo/1_4_1_2.html

> **2.模板短信SDK使用说明**

* http://doc.yuntongxun.com/p/5a533e0c3b8496dd00dce08c

> **3.集成模板短信SDK**
* `CCPRestSDK.py`：由容联云通讯开发者编写的官方SDK文件，包括发送模板短信的方法
* `ccp_sms.py`：调用发送模板短信的方法

<img src="/user-verification-code/images/21集成模板短信SDK.png" style="zoom:50%">

> **4.模板短信SDK测试**
* `ccp_sms.py`文件中
    
```python
# -*- coding:utf-8 -*-

from verifications.libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8aaf070862181ad5016236f3bcc811d5'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '4e831592bd464663b0de944df13f16ef'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf070868747811016883f12ef3062c'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    print(result)
    for k, v in result.items():

        if k == 'templateSMS':
            for k, s in v.items():
                print('%s:%s' % (k, s))
        else:
            print('%s:%s' % (k, v))

if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    sendTemplateSMS('17600992168', ['123456', 5], 1)
```

> **5.模板短信SDK返回结果说明**

```json
{
    'statusCode': '000000', // 状态码。'000000'表示成功，反之，失败
    'templateSMS': 
        {
            'smsMessageSid': 'b5768b09e5bc4a369ed35c444c13a1eb', // 短信唯一标识符
            'dateCreated': '20190125185207' // 短信发送时间
        }
}
```

### 3. 封装发送短信单例类

> **1.封装发送短信单例类**

```python
class CCP(object):
    """发送短信的单例类"""

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        return cls._instance
```

> **2.封装发送短信单例方法**

```python
def send_template_sms(self, to, datas, temp_id):
    """
    发送模板短信单例方法
    :param to: 注册手机号
    :param datas: 模板短信内容数据，格式为列表，例如：['123456', 5]，如不需替换请填 ''
    :param temp_id: 模板编号，默认免费提供id为1的模板
    :return: 发短信结果
    """
    result = self.rest.sendTemplateSMS(to, datas, temp_id)
    if result.get("statusCode") == "000000":
        # 返回0，表示发送短信成功
        return 0
    else:
        # 返回-1，表示发送失败
        return -1
```

> **3.测试单例类发送模板短信结果**

```python
if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    CCP().send_template_sms('17600992168', ['123456', 5], 1)
```

### 4. 知识要点

1. 容联云通讯只是发送短信的平台之一，还有其他云平台可用，比如，阿里云等，实现套路都是相通的。
2. 将发短信的类封装为单例，属于性能优化的一种方案。



