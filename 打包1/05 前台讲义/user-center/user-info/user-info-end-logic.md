# 查询并渲染用户基本信息

### 1. 用户模型补充email_active字段

> * 由于在渲染用户基本信息时，需要渲染用户邮箱验证的状态，所以需要给**用户模型补充email_active字段**

> * 补充完字段后，需要进行迁移。
    ```bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

```python
class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
```

### 2. 查询用户基本信息

```python
class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context=context)
```

### 3. 渲染用户基本信息

> **1.将后端模板数据传递到Vue.js**
* 为了方便实现用户添加邮箱时的界面局部刷新
    * 我们将后端提供的用户数据传入到`user_center_info.js`中

```js
<script type="text/javascript">
    let username = "{{ username }}";
    let mobile = "{{ mobile }}";
    let email = "{{ email }}";
    let email_active = "{{ email_active }}";
</script>
<script type="text/javascript" src="{{ static('js/common.js') }}"></script>
<script type="text/javascript" src="{{ static('js/user_center_info.js') }}"></script>
```

```js
data: {
    username: username,
    mobile: mobile,
    email: email,
    email_active: email_active,
},
```

> **2.Vue渲染用户基本信息：`user_center_info.html`**

```html
<div class="info_con clearfix" v-cloak>
    <h3 class="common_title2">基本信息</h3>
    <ul class="user_info_list">
        <li><span>用户名：</span>[[ username ]]</li>
        <li><span>联系方式：</span>[[ mobile ]]</li>
        <li>
            <span>Email：</span>
            <div v-if="set_email">
                <input v-model="email" @blur="check_email" type="email" name="email" class="email">
                <input @click="save_email" type="button" name="" value="保 存">
                <input @click="cancel_email" type="reset" name="" value="取 消">
                <div v-show="error_email" class="error_email_tip">邮箱格式错误</div>
            </div>
            <div v-else>
                <input v-model="email" type="email" name="email" class="email" readonly>
                <div v-if="email_active">
                    已验证
                </div>
                <div v-else>
                    待验证<input @click="save_email" :disabled="send_email_btn_disabled" type="button" :value="send_email_tip">
                </div>
            </div>
        </li>
    </ul>
</div>
```
