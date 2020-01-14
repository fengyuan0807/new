# 用户注册前端逻辑

> **为了学会使用Vue.js的双向绑定实现用户的交互和页面局部刷新效果。**

### 1. 用户注册页面绑定Vue数据

> **1.准备div盒子标签**

```html
<div id="app">
    <body>
    ......
    </body>
</div>
```

> **2.register.html**
* 绑定内容：变量、事件、错误提示等

```html
<form method="post" class="register_form" @submit="on_submit" v-cloak>
    {{ csrf_input }}
    <ul>
        <li>
            <label>用户名:</label>
            <input type="text" v-model="username" @blur="check_username" name="username" id="user_name">
            <span class="error_tip" v-show="error_name">[[ error_name_message ]]</span>
        </li>
        <li>
            <label>密码:</label>
            <input type="password" v-model="password" @blur="check_password" name="password" id="pwd">
            <span class="error_tip" v-show="error_password">请输入8-20位的密码</span>
        </li>
        <li>
            <label>确认密码:</label>
            <input type="password" v-model="password2" @blur="check_password2" name="password2" id="cpwd">
            <span class="error_tip" v-show="error_password2">两次输入的密码不一致</span>
        </li>
        <li>
            <label>手机号:</label>
            <input type="text" v-model="mobile" @blur="check_mobile" name="mobile" id="phone">
            <span class="error_tip" v-show="error_mobile">[[ error_mobile_message ]]</span>
        </li>
        <li>
            <label>图形验证码:</label>
            <input type="text" name="image_code" id="pic_code" class="msg_input">
            <img src="{{ static('images/pic_code.jpg') }}" alt="图形验证码" class="pic_code">
            <span class="error_tip">请填写图形验证码</span>
        </li>
        <li>
            <label>短信验证码:</label>
            <input type="text" name="sms_code" id="msg_code" class="msg_input">
            <a href="javascript:;" class="get_msg_code">获取短信验证码</a>
            <span class="error_tip">请填写短信验证码</span>
        </li>
        <li class="agreement">
            <input type="checkbox" v-model="allow" @change="check_allow" name="allow" id="allow">
            <label>同意”美多商城用户使用协议“</label>
            <span class="error_tip2" v-show="error_allow">请勾选用户协议</span>
        </li>
        <li class="reg_sub">
            <input type="submit" value="注 册">
        </li>
    </ul>
</form>
```

### 2. 用户注册JS文件实现用户交互

> **1.导入Vue.js库和ajax请求的库**

```html
<script type="text/javascript" src="{{ static('js/vue-2.5.16.js') }}"></script>
<script type="text/javascript" src="{{ static('js/axios-0.18.0.min.js') }}"></script>
```

> **2.准备register.js文件**

```js
<script type="text/javascript" src="{{ static('js/register.js') }}"></script>
```

> 绑定内容：变量、事件、错误提示等

```js
let vm = new Vue({
    el: '#app',
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',

        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,

        error_name_message: '',
        error_mobile_message: '',
    },
    methods: {
        // 校验用户名
        check_username(){
        },
        // 校验密码
        check_password(){
        },
        // 校验确认密码
        check_password2(){
        },
        // 校验手机号
        check_mobile(){
        },
        // 校验是否勾选协议
        check_allow(){
        },
        // 监听表单提交事件
        on_submit(){
        },
    }
});
```

> **3.用户交互事件实现**

```js
methods: {
    // 校验用户名
    check_username(){
        let re = /^[a-zA-Z0-9_-]{5,20}$/;
        if (re.test(this.username)) {
            this.error_name = false;
        } else {
            this.error_name_message = '请输入5-20个字符的用户名';
            this.error_name = true;
        }
    },
    // 校验密码
    check_password(){
        let re = /^[0-9A-Za-z]{8,20}$/;
        if (re.test(this.password)) {
            this.error_password = false;
        } else {
            this.error_password = true;
        }
    },
    // 校验确认密码
    check_password2(){
        if(this.password != this.password2) {
            this.error_password2 = true;
        } else {
            this.error_password2 = false;
        }
    },
    // 校验手机号
    check_mobile(){
        let re = /^1[3-9]\d{9}$/;
        if(re.test(this.mobile)) {
            this.error_mobile = false;
        } else {
            this.error_mobile_message = '您输入的手机号格式不正确';
            this.error_mobile = true;
        }
    },
    // 校验是否勾选协议
    check_allow(){
        if(!this.allow) {
            this.error_allow = true;
        } else {
            this.error_allow = false;
        }
    },
    // 监听表单提交事件
    on_submit(){
        this.check_username();
        this.check_password();
        this.check_password2();
        this.check_mobile();
        this.check_allow();

        if(this.error_name == true || this.error_password == true || this.error_password2 == true
            || this.error_mobile == true || this.error_allow == true) {
            // 禁用表单的提交
            window.event.returnValue = false;
        }
    },
}
```

### 4. 知识要点

1. Vue绑定页面的套路
    * 导入Vue.js库和ajax请求的库
    * 准备div盒子标签
    * 准备js文件
    * html页面绑定变量、事件等
    * js文件定义变量、事件等
2. 错误提示
    * 如果错误提示信息是固定的，可以把错误提示信息写死，再通过v-show控制是否展示
    * 如果错误提示信息不是固定的，可以使用绑定的变量动态的展示错误提示信息，再通过v-show控制是否展示
3. 修改Vue变量的读取语法，避免和Django模板语法冲突
    * `delimiters: ['[[', ']]']`
4. 后续的页面中如果有类似的交互和刷新效果，也可按照此套路实现












