# 图形验证码前端逻辑

### 1. Vue实现图形验证码展示

> **1.register.js**

```js
mounted(){
    // 生成图形验证码
    this.generate_image_code();
},
methods: {
    // 生成图形验证码
    generate_image_code(){
        // 生成UUID。generateUUID() : 封装在common.js文件中，需要提前引入
        this.uuid = generateUUID();
        // 拼接图形验证码请求地址
        this.image_code_url = "/image_codes/" + this.uuid + "/";
    },
    ......
}
```

> **2.register.html**

```html
<li>
    <label>图形验证码:</label>
    <input type="text" name="image_code" id="pic_code" class="msg_input">
    <img :src="image_code_url" @click="generate_image_code" alt="图形验证码" class="pic_code">
    <span class="error_tip">请填写图形验证码</span>
</li>
```

> **3.图形验证码展示和存储效果**

<img src="/user-verification-code/images/05图形验证码展示效果.png" style="zoom:50%">

<img src="/user-verification-code/images/06图形验证码存储效果.png" style="zoom:50%">

### 2. Vue实现图形验证码校验

> **1.register.html**

```html
<li>
    <label>图形验证码:</label>
    <input type="text" v-model="image_code" @blur="check_image_code" name="image_code" id="pic_code" class="msg_input">
    <img :src="image_code_url" @click="generate_image_code" alt="图形验证码" class="pic_code">
    <span class="error_tip" v-show="error_image_code">[[ error_image_code_message ]]</span>
</li>
```

> **2.register.js**

```js
check_image_code(){
    if(!this.image_code) {
        this.error_image_code_message = '请填写图片验证码';
        this.error_image_code = true;
    } else {
        this.error_image_code = false;
    }
},
```

> **3.图形验证码校验效果**

<img src="/user-verification-code/images/07图形验证码校验效果.png" style="zoom:50%">

