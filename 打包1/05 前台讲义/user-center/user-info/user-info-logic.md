# 用户基本信息逻辑分析

### 1. 用户基本信息逻辑分析

<img src="/user-center/images/01用户基本信息逻辑分析1.png" style="zoom:50%">

<img src="/user-center/images/02用户基本信息逻辑分析2.png" style="zoom:50%">

<img src="/user-center/images/03用户基本信息逻辑分析3.png" style="zoom:50%">

<img src="/user-center/images/04用户基本信息逻辑分析4.png" style="zoom:50%">

> 以下是要实现的后端逻辑

1. 用户模型补充`email_active`字段
2. 查询并渲染用户基本信息
3. 添加邮箱
4. 发送邮箱验证邮件
5. 验证邮箱

> 提示：

* 用户添加邮箱时，界面的局部刷新，我们选择使用`Vue.js`来实现。
