# 修改地址前后端逻辑

### 1. 修改地址接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /addresses/(?P&lt;address_id&gt;\d+)/ |

> **2.请求参数：路径参数 和 JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **address_id** | string | 是 | 要修改的地址ID（路径参数） |
| **receiver** | string | 是 | 收货人 |
| **province_id** | string | 是 | 省份ID |
| **city_id** | string | 是 | 城市ID |
| **district_id** | string | 是 | 区县ID |
| **place** | string | 是 | 收货地址 |
| **mobile** | string | 是 | 手机号 |
| **tel** | string | 否 | 固定电话 |
| **email** | string | 否 | 邮箱 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **id** | 地址ID |
| **receiver** | 收货人 |
| **province** | 省份名称 |
| **city** | 城市名称 |
| **district** | 区县名称 |
| **place** | 收货地址 |
| **mobile** | 手机号 |
| **tel** | 固定电话 |
| **email** | 邮箱 |

### 2. 修改地址后端逻辑实现

> 提示 
* 删除地址后端逻辑和新增地址后端逻辑非常的相似。
* 都是更新用户地址模型类，需要保存用户地址信息。

```python
class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user = request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
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

        # 响应更新地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})
```

### 3. 修改地址前端逻辑实现

> **1.添加修改地址的标记**

* 新增地址和修改地址的交互不同。
* 为了区分用户是新增地址还是修改地址，我们可以选择添加一个变量，作为标记。
* 为了方便得到正在修改的地址信息，我们可以选择展示地址时对应的序号作为标记。

```js
data: {
    editing_address_index: '', 
},
```

> **2.实现`编辑`按钮对应的事件**

```js
show_edit_site(index){
    this.is_show_edit = true;
    this.clear_all_errors();
    this.editing_address_index = index.toString();
},
```

```html
<div class="down_btn">
    <a v-if="address.id!=default_address_id">设为默认</a>
    <a href="javascript:;" class="edit_icon">编辑</a>
</div>
```

> **3.展示要重新编辑的数据**

```js
show_edit_site(index){
    this.is_show_edit = true;
    this.clear_all_errors();
    this.editing_address_index = index.toString();
    // 只获取要编辑的数据
    this.form_address = JSON.parse(JSON.stringify(this.addresses[index]));
},
```

> **4.发送修改地址请求**
* 重要提示：
    * `0 == ''` 返回`true`
    * `0 === ''` 返回`false`
    * 为了避免第0个索引出错，我们选择`this.editing_address_index === ''`的方式进行判断

```js
if (this.editing_address_index === '') {
    // 新增地址
    ......
} else {
    // 修改地址
    let url = '/addresses/' + this.addresses[this.editing_address_index].id + '/';
    axios.put(url, this.form_address, {
        headers: {
            'X-CSRFToken':getCookie('csrftoken')
        },
        responseType: 'json'
    })
        .then(response => {
            if (response.data.code == '0') {
                this.addresses[this.editing_address_index] = response.data.address;
                this.is_show_edit = false;
            } else if (response.data.code == '4101') {
                location.href = '/login/?next=/addresses/';
            } else {
                alert(response.data.errmsg);
            }
        })
        .catch(error => {
            alert(error.response);
        })
}
```