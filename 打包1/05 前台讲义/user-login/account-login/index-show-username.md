# 首页用户名展示

<img src="/user-login/images/04主页用户名信息展示效果.png" style="zoom:50%">

### 1. 首页用户名展示方案

> 方案一
* 模板中 **request** 变量直接渲染用户名
* 缺点：不方便做首页静态化

```html
{% if user.is_authenticated %}
    <div class="login_btn fl">
        欢迎您：<em>{{ user.username }}</em>
        <span>|</span>
        <a href="#">退出</a>
    </div>
    {% else %}
    <div class="login_btn fl">
        <a href="login.html">登录</a>
        <span>|</span>
        <a href="register.html">注册</a>
    </div>
{% endif %}
```

> 方案二
* 发送ajax请求获取用户信息
* 缺点：需要发送网络请求

```html
<div class="login_btn fl">
    {# ajax渲染 #}
</div>
```

> 方案三
* Vue读取cookie渲染用户信息

```html
<div v-if="username" class="login_btn fl">
    欢迎您：<em>[[ username ]]</em>
    <span>|</span>
    <a href="#">退出</a>
</div>
<div v-else class="login_btn fl">
    <a href="login.html">登录</a>
    <span>|</span>
    <a href="register.html">注册</a>
</div>
```

> 结论：
* 对比此三个方案，我们在本项目中选择 **方案三**

> 实现步骤：
* 注册或登录后，用户名写入到cookie
* Vue渲染主页用户名

### 2. 用户名写入到cookie

```python
# 响应注册结果
response = redirect(reverse('contents:index'))

# 注册时用户名写入到cookie，有效期15天
response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

return response
```

```python
# 响应登录结果
response = redirect(reverse('contents:index'))

# 登录时用户名写入到cookie，有效期15天
response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

return response
```

### 3. Vue渲染首页用户名

> **1.index.html**

```html
<div v-if="username" class="login_btn fl">
    欢迎您：<em>[[ username ]]</em>
    <span>|</span>
    <a href="#">退出</a>
</div>
<div v-else class="login_btn fl">
    <a href="login.html">登录</a>
    <span>|</span>
    <a href="register.html">注册</a>
</div>
```

> **2.index.js**

```js
mounted(){
    // 获取cookie中的用户名
    this.username = getCookie('username');
},
```