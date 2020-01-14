# 退出登录

### 1. logout()方法介绍

1. 退出登录：
    * 回顾登录：将通过认证的用户的唯一标识信息，写入到当前session会话中
    * 退出登录：正好和登录相反（清理session会话信息）

2. logout()方法：
    * Django用户认证系统提供了`logout()`方法
    * 封装了清理session的操作，帮助我们快速实现登出一个用户

3. logout()位置：
    * `django.contrib.auth.__init__.py`文件中
    
```python
logout(request)
```

### 2. logout()方法使用

```python
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = redirect(reverse('contents:index'))
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response
```

### 3. 知识要点

1. 退出登录的核心思想就是清理登录时缓存的状态保持信息。
2. 由于首页中用户名是从cookie中读取的。所以退出登录时，需要将cookie中用户名清除。
