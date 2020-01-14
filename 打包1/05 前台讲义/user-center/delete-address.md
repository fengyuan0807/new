# 删除地址前后端逻辑

### 1. 删除地址接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | DELETE |
| **请求地址** | /addresses/(?P&lt;address_id&gt;\d+)/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **address_id** | string | 是 | 要修改的地址ID（路径参数） |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

### 2. 删除地址后端逻辑实现

> 提示：
* 删除地址不是物理删除，是逻辑删除。

```python
class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """修改地址"""
        ......

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})
```

### 3. 删除地址前端逻辑实现

```js
delete_address(index){
    let url = '/addresses/' + this.addresses[index].id + '/';
    axios.delete(url, {
        headers: {
            'X-CSRFToken':getCookie('csrftoken')
        },
        responseType: 'json'
    })
        .then(response => {
            if (response.data.code == '0') {
                // 删除对应的标签
                this.addresses.splice(index, 1);
            } else if (response.data.code == '4101') {
                location.href = '/login/?next=/addresses/';
            }else {
                alert(response.data.errmsg);
            }
        })
        .catch(error => {
            console.log(error.response);
        })
},
```

```html
<div class="site_title">
    <h3>[[ address.title ]]</h3>
    <a href="javascript:;" class="edit_icon"></a>
    <em v-if="address.id===default_address_id">默认地址</em>
    <span @click="delete_address(index)" class="del_site">×</span>
</div>
```