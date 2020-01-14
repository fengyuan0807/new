# 修改地址标题

### 1. 修改地址标题接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /addresses/(?P&lt;address_id&gt;\d+)/title/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **address_id** | string | 是 | 要修改的地址ID（路径参数） |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |


### 2. 修改地址标题后端逻辑实现

```python
class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置地址标题成功'})
```

### 3. 修改地址标题前端逻辑实现

<img src="/user-center/images/12设置地址标题1.png" style="zoom:50%">
<img src="/user-center/images/12设置地址标题2.png" style="zoom:50%">
<img src="/user-center/images/12设置地址标题3.png" style="zoom:50%">

```html
<div class="site_title">
    <div v-if="edit_title_index===index">
        <input v-model="new_title" type="text" name="">
        <input @click="save_title(index)" type="button" name="" value="保 存">
        <input @click="cancel_title(index)" type="reset" name="" value="取 消">
    </div>
    <div>
        <h3>[[ address.title ]]</h3>
        <a @click="show_edit_title(index)" class="edit_title"></a>
    </div>
    <em v-if="address.id===default_address_id">默认地址</em>
    <span @click="delete_address(index)">×</span>
</div>
```

```js
data: {
    edit_title_index: '',
    new_title: '',
},
```

```js
// 展示地址title编辑框
show_edit_title(index){
    this.edit_title_index = index;
},
// 取消保存地址title
cancel_title(){
    this.edit_title_index = '';
    this.new_title = '';
},
// 修改地址title
save_title(index){
    if (!this.new_title) {
        alert("请填写标题后再保存！");
    } else {
        let url = '/addresses/' + this.addresses[index].id + '/title/';
        axios.put(url, {
            title: this.new_title
        }, {
            headers: {
                'X-CSRFToken':getCookie('csrftoken')
            },
            responseType: 'json'
        })
            .then(response => {
                if (response.data.code == '0') {
                    // 更新地址title
                    this.addresses[index].title = this.new_title;
                    this.cancel_title();
                } else if (response.data.code == '4101') {
                    location.href = '/login/?next=/addresses/';
                } else {
                    alert(response.data.errmsg);
                }
            })
            .catch(error => {
                console.log(error.response);
            })
    }
},
```