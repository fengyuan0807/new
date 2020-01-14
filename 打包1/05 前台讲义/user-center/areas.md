# 省市区三级联动

### 1. 展示收货地址界面

> 提示：
* 省市区数据是在收货地址界面展示的，所以我们先渲染出收货地址界面。
* 收货地址界面中基础的交互已经提前实现。

```python
class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        return render(request, 'user_center_site.html')
```

### 2. 准备省市区模型和数据

```python
class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name
```

> 模型说明：

* 自关联字段的外键指向自身，所以 `models.ForeignKey('self')`
* 使用`related_name`指明父级查询子级数据的语法
    * 默认`Area模型类对象.area_set`语法
* `related_name='subs'`
    * 现在`Area模型类对象.subs`语法

> 导入省市区数据

```bash
mysql -h数据库ip地址 -u数据库用户名 -p数据库密码 数据库 < areas.sql
mysql -h127.0.0.1 -uroot -pmysql meiduo_mall < areas.sql
```

### 3. 查询省市区数据

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /areas/ |

> **2.请求参数：查询参数**
* 如果前端没有传入`area_id`，表示用户需要省份数据
* 如果前端传入了`area_id`，表示用户需要市或区数据

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **area_id** | string | 否 | 地区ID |

> **3.响应结果：JSON**

* 省份数据
```json
{
    "code":"0",
    "errmsg":"OK",
    "province_list":[
        {
            "id":110000,
            "name":"北京市"
        },
        {
            "id":120000,
            "name":"天津市"
        },
        {
            "id":130000,
            "name":"河北省"
        },
        ......
    ]
}
```

* 市或区数据
```json
{
    "code":"0",
    "errmsg":"OK",
    "sub_data":{
        "id":130000,
        "name":"河北省",
        "subs":[
            {
                "id":130100,
                "name":"石家庄市"
            },
            ......
        ]
    }
}
```

> **4.查询省市区数据后端逻辑实现**
* 如果前端没有传入`area_id`，表示用户需要省份数据
* 如果前端传入了`area_id`，表示用户需要市或区数据

```python
class AreasView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            # 提供省份数据
            try:
                # 查询省份数据
                province_model_list = Area.objects.filter(parent__isnull=True)

                # 序列化省级数据
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})

            # 响应省份数据
            return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
        else:
            # 提供市或区数据
            try:
                parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list = []
                for sub_model in sub_model_list:
                    sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                sub_data = {
                    'id': parent_model.id,  # 父级pk
                    'name': parent_model.name,  # 父级name
                    'subs': sub_list  # 父级的子集
                }
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})

            # 响应市或区数据
            return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})
```

### 4. Vue渲染省市区数据

> **1.`user_center_site.js`中**

```js
mounted() {
    // 获取省份数据
    this.get_provinces();
},
```

```js
// 获取省份数据
get_provinces(){
    let url = '/areas/';
    axios.get(url, {
        responseType: 'json'
    })
        .then(response => {
            if (response.data.code == '0') {
                this.provinces = response.data.province_list;
            } else {
                console.log(response.data);
                this.provinces = [];
            }
        })
        .catch(error => {
            console.log(error.response);
            this.provinces = [];
        })
},
```

```js
watch: {
    // 监听到省份id变化
    'form_address.province_id': function(){
        if (this.form_address.province_id) {
            let url = '/areas/?area_id=' + this.form_address.province_id;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.cities = response.data.sub_data.subs;
                    } else {
                        console.log(response.data);
                        this.cities = [];
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.cities = [];
                })
        }
    },
    // 监听到城市id变化
    'form_address.city_id': function(){
        if (this.form_address.city_id){
            let url = '/areas/?area_id='+ this.form_address.city_id;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.districts = response.data.sub_data.subs;
                    } else {
                        console.log(response.data);
                        this.districts = [];
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.districts = [];
                })
        }
    }
},
```

> **2.`user_center_site.html`中**

```html
<div class="form_group">
    <label>*所在地区：</label>
    <select v-model="form_address.province_id">
        <option v-for="province in provinces" :value="province.id">[[ province.name ]]</option>
    </select>
    <select v-model="form_address.city_id">
        <option v-for="city in cities" :value="city.id">[[ city.name ]]</option>
    </select>
    <select v-model="form_address.district_id">
        <option v-for="district in districts" :value="district.id">[[ district.name ]]</option>
    </select>
</div>
```

### 5. 缓存省市区数据

> 提示：

* 省市区数据是我们动态查询的结果。
* 但是省市区数据不是频繁变化的数据，所以没有必要每次都重新查询。
* 所以我们可以选择对省市区数据进行缓存处理。

> **1.缓存工具**

* `from django.core.cache import cache`
* 存储缓存数据：`cache.set('key', 内容, 有效期)`
* 读取缓存数据：`cache.get('key')`
* 删除缓存数据：`cache.delete('key')`
* **注意：存储进去和读取出来的数据类型相同，所以读取出来后可以直接使用。**

> **2.缓存逻辑**

<img src="/user-center/images/11缓存逻辑.png" style="zoom:50%">

> **3.缓存逻辑实现**
* 省份缓存数据
    * `cache.set('province_list', province_list, 3600)`
* 市或区缓存数据
    * `cache.set('sub_area_' + area_id, sub_data, 3600)`

```python
class AreasView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            # 读取省份缓存数据
            province_list = cache.get('province_list')

            if not province_list:
                # 提供省份数据
                try:
                    # 查询省份数据
                    province_model_list = Area.objects.filter(parent__isnull=True)

                    # 序列化省级数据
                    province_list = []
                    for province_model in province_model_list:
                        province_list.append({'id': province_model.id, 'name': province_model.name})
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})

                # 存储省份缓存数据
                cache.set('province_list', province_list, 3600)

            # 响应省份数据
            return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})
        else:
            # 读取市或区缓存数据
            sub_data = cache.get('sub_area_' + area_id)

            if not sub_data:
                # 提供市或区数据
                try:
                    parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                    sub_model_list = parent_model.subs.all()

                    # 序列化市或区数据
                    sub_list = []
                    for sub_model in sub_model_list:
                        sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                    sub_data = {
                        'id': parent_model.id,  # 父级pk
                        'name': parent_model.name,  # 父级name
                        'subs': sub_list  # 父级的子集
                    }
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})

                # 储存市或区缓存数据
                cache.set('sub_area_' + area_id, sub_data, 3600)

            # 响应市或区数据
            return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})
```


