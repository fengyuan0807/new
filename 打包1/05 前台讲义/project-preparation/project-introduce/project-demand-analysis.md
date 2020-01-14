# 项目需求分析

> 需求分析原因：
* 可以整体的了解项目的业务流程和主要的业务需求。
* 项目中，**需求驱动开发**。即开发人员需要以需求为目标来实现业务逻辑。

> 需求分析方式：
* 企业中，借助 **产品原型图** 分析需求。
* 需求分析完后，前端按照产品原型图开发前端页面，**后端开发对应的业务及响应处理**。

> 需求分析内容：
* 页面及其**业务流程和业务逻辑**。

> 提示：
* 我们现在借助 **示例网站** 作为原型图来分析需求。
    
### 1. 项目主要页面介绍

> **1.首页广告**

![](/project-preparation/images/08首页广告.png)

> **2.注册**

![](/project-preparation/images/01注册.png)
    
> **3.登录**

![](/project-preparation/images/02登录.png)
    
> **4.QQ登录**

![](/project-preparation/images/03QQ登录.png)

![](/project-preparation/images/03QQ用户绑定.png)
    
> **5.个人信息**

![](/project-preparation/images/04个人信息.png)
    
> **6.收货地址**

![](/project-preparation/images/05收货地址.png)

> **7.我的订单**

![](/project-preparation/images/06我的订单.png)

> **8.修改密码**

![](/project-preparation/images/07修改密码.png)

> **9.商品列表**

![](/project-preparation/images/09商品列表.png)

> **10.商品搜索**

![](/project-preparation/images/10商品搜索.png)

> **11.商品详情**

![](/project-preparation/images/11商品详情.png)

> **12.购物车**

![](/project-preparation/images/12购物车.png)

> **13.结算订单**

![](/project-preparation/images/13结算订单.png)

> **14.提交订单**

![](/project-preparation/images/14提交订单成功.png)

> **15.支付宝支付**

![](/project-preparation/images/15支付宝支付.png)

> **16.支付结果处理**

![](/project-preparation/images/16支付成功.png)

> **17.订单商品评价**

![](/project-preparation/images/17订单商品评价.png)

### 2. 归纳项目主要模块

> 为了方便项目管理及多人协同开发，我们根据需求将功能划分为不同的模块。

> 将来在项目中，每个**`模块`**都会对应一个**`子应用`**进行**`管理和解耦`**。

| 模块 | 功能 |
| ---------------- | ---------------- |
| **验证** | 图形验证、短信验证 |
| **用户** | 注册、登录、用户中心 |
| **第三方登录** | QQ登录 |
| **首页广告** | 首页广告 |
| **商品** | 商品列表、商品搜索、商品详情 |
| **购物车** | 购物车管理、购物车合并 |
| **订单** | 确认订单、提交订单 |
| **支付** | 支付宝支付、订单商品评价 |
| **MIS系统** | 数据统计、用户管理、权限管理、商品管理、订单管理 |

### 3. 知识要点

1. 需求分析原因：需求驱动开发。
2. 需求分析方式：企业中，使用产品原型图。
3. 需求分析内容：页面及业务逻辑。
4. 需求分析结果：划分业务模块，明确每个模块下的主要功能，并以子应用的形式进行管理。


