# 设置默认地址

### 1. 设置默认地址接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /addresses/(?P&lt;address_id&gt;\d+)/default/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **address_id** | string | 是 | 要修改的地址ID（路径参数） |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

### 2. 设置默认地址后端逻辑实现

```python
class DefaultAddressView(LoginRequiredJSONMixin, View):
    """设置默认地址"""

    def put(self, request, address_id):
        """设置默认地址"""
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)

            # 设置地址为默认地址
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})

        # 响应设置默认地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})
```

### 3. 设置默认地址前端逻辑实现

```js
set_default(index){
    let url = '/addresses/' + this.addresses[index].id + '/default/';
    axios.put(url, {}, {
        headers: {
            'X-CSRFToken':getCookie('csrftoken')
        },
        responseType: 'json'
    })
        .then(response => {
            if (response.data.code == '0') {
                // 设置默认地址标签
                this.default_address_id = this.addresses[index].id;
            } else if (response.data.code == '4101') {
                location.href = '/login/?next=/addresses/';
            } else {
                alert(response.data.errmsg);
            }
        })
        .catch(error => {
            console.log(error.response);
        })
},
```

```html
<div class="down_btn">
    <a v-if="address.id!=default_address_id" @click="set_default(index)">设为默认</a>
    <a @click="show_edit_site(index)" class="edit_icon">编辑</a>
</div>
```