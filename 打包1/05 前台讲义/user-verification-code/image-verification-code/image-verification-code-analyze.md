# 图形验证码逻辑分析

<img src="/user-verification-code/images/01图形验证码逻辑分析.png" style="zoom:50%">

> 需要新建应用`verifications`

### 知识要点

1. 将图形验证码的文字信息保存到Redis数据库，为短信验证码做准备。
2. UUID 用于唯一区分该图形验证码属于哪个用户，也可使用其他唯一标识信息来实现。
