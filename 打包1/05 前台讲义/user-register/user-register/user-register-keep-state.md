# 状态保持

> 说明：
* 如果需求是注册成功后即表示用户登入成功，那么此时可以在注册成功后实现状态保持
* 如果需求是注册成功后不表示用户登入成功，那么此时不用在注册成功后实现状态保持

> **美多商城的需求是：注册成功后即表示用户登入成功**

### 1. login()方法介绍

1. 用户登入本质：
    * **状态保持**
    * 将通过认证的用户的唯一标识信息（比如：用户ID）写入到当前浏览器的 cookie 和服务端的 session 中。
2. login()方法：
    * Django用户认证系统提供了`login()`方法。
    * 封装了写入session的操作，帮助我们快速登入一个用户，并实现状态保持。
3. login()位置：
    * `django.contrib.auth.__init__.py`文件中。
    
    ```python
    login(request, user, backend=None)
    ```
4. 状态保持 session 数据存储的位置：**Redis数据库的1号库**
    ```python
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "session"
    ```

### 2. login()方法登入用户

```python
# 保存注册数据
try:
    user = User.objects.create_user(username=username, password=password, mobile=mobile)
except DatabaseError:
    return render(request, 'register.html', {'register_errmsg': '注册失败'})

# 登入用户，实现状态保持
login(request, user)

# 响应注册结果
return redirect(reverse('contents:index'))
```

### 3. 查看状态保持结果

<img src="/user-register/images/12session浏览器.png" style="zoom:50%">

<img src="/user-register/images/13sessionredis.png" style="zoom:50%">

### 4. 知识要点

1. 登入用户，并实现状态保持的方式：`login(request, user, backend=None)`