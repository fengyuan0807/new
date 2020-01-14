# 展示地址前后端逻辑

### 1. 展示地址接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /addresses/ |

> **2.请求参数**

```
无
```

> **3.响应结果：HTML**

```python
user_center_site.html
```

### 2. 展示地址后端逻辑实现

```python
class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        # 获取用户地址列表
        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, 'user_center_site.html', context)
```

### 3. 展示地址前端逻辑实现

> **1.将后端模板数据传递到Vue.js**

```js
<script type="text/javascript">
    let addresses = {{ addresses | safe }};
    let default_address_id = "{{ default_address_id }}";
</script>
```

```js
data: {
    addresses: JSON.parse(JSON.stringify(addresses)),
    default_address_id: default_address_id,
},
```

> **2.`user_center_site.html`中渲染地址信息**

```html
<div class="right_content clearfix" v-cloak>
    <div class="site_top_con">
        <a @click="show_add_site">新增收货地址</a>
        <span>你已创建了<b>[[ addresses.length ]]</b>个收货地址，最多可创建<b>20</b>个</span>
    </div>
    <div class="site_con" v-for="(address, index) in addresses">
        <div class="site_title">
            <h3>[[ address.title ]]</h3>
            <a href="javascript:;" class="edit_icon"></a>
            <em v-if="address.id===default_address_id">默认地址</em>
            <span class="del_site">×</span>
        </div>
        <ul class="site_list">
            <li><span>收货人：</span><b>[[ address.receiver ]]</b></li>
            <li><span>所在地区：</span><b>[[ address.province ]] [[address.city]] [[ address.district ]]</b></li>
            <li><span>地址：</span><b>[[ address.place ]]</b></li>
            <li><span>手机：</span><b>[[ address.mobile ]]</b></li>
            <li><span>固定电话：</span><b>[[ address.tel ]]</b></li>
            <li><span>电子邮箱：</span><b>[[ address.email ]]</b></li>
        </ul>
        <div class="down_btn">
            <a v-if="address.id!=default_address_id">设为默认</a>
            <a href="javascript:;" class="edit_icon">编辑</a>
        </div>
    </div>
</div>
```

> **3.完善`user_center_site.js`中成功新增地址后的局部刷新**

```js
if (response.data.code == '0') {
    // 局部刷新界面：展示所有地址信息，将新的地址添加到头部
    this.addresses.splice(0, 0, response.data.address);
    this.is_show_edit = false;
} 
```