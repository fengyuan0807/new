# 新增地址前后端逻辑

### 1. 定义用户地址模型类

> **1.用户地址模型类**

```python
class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
```

> **2.`Address`模型类说明**

* `Address`模型类中的外键指向`areas/models`里面的`Area`。指明外键时，可以使用`应用名.模型类名`来定义。
* `ordering` 表示在进行`Address`查询时，默认使用的排序方式。
    * `ordering = ['-update_time']` : 根据更新的时间倒叙。

> **3.补充用户模型默认地址字段**

```python
class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
```

### 2. 新增地址接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /addresses/create/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
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

### 3. 新增地址后端逻辑实现

> 提示：
* 用户地址数量有上限，最多20个，超过地址数量上限就返回错误信息

```python
class CreateAddressView(LoginRequiredJSONMixin, View):
    """新增地址"""

    def post(self, request):
        """实现新增地址逻辑"""
        # 判断是否超过地址上限：最多20个
        # Address.objects.filter(user=request.user).count()
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})

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

        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
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

            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
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

        # 响应保存结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address':address_dict})
```

### 4. 新增地址前端逻辑实现

```js
save_address(){
    if (this.error_receiver || this.error_place || this.error_mobile || this.error_email || !this.form_address.province_id || !this.form_address.city_id || !this.form_address.district_id ) {
        alert('信息填写有误！');
    } else {
        // 新增地址
        let url = '/addresses/create/';
        axios.post(url, this.form_address, {
            headers: {
                'X-CSRFToken':getCookie('csrftoken')
            },
            responseType: 'json'
        })
            .then(response => {
                if (response.data.code == '0') {
                    // 局部刷新界面：展示所有地址信息
                    
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