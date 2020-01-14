# 保存订单支付结果

### 1. 支付结果数据说明

* 用户订单支付成功后，支付宝会将用户重定向到 `http://www.meiduo.site:8000/payment/status/
`，并携带支付结果数据。

* 参考统一收单下单并支付页面接口：https://docs.open.alipay.com/270/alipay.trade.page.pay

    <img src="/payment/images/12页面回跳参数.png" style="zoom:50%">

> 提示：

> 我们需要将**`订单编号`**和**`交易流水号`**进行关联存储，方便用户和商家后续使用。

### 2. 定义支付结果模型类

```python
class Payment(BaseModel):
    """支付信息"""
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="支付编号")

    class Meta:
        db_table = 'tb_payment'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name
```

### 3. 保存订单支付结果

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /payment/status/ |

> **2.请求参数：路径参数**

```
参考统一收单下单并支付页面接口中的《页面回跳参数》
```

> **3.响应结果：HTML**

```
pay_success.html
```

> **4.后端接口定义和实现**

> 注意：保存订单支付结果的同时，还需要修改订单的状态为**`待评价`**

```python
# 测试账号：pqcanx4910@sandbox.com
class PaymentStatusView(View):
    """保存订单支付结果"""

    def get(self, request):
        # 获取前端传入的请求参数
        query_dict = request.GET
        data = query_dict.dict()
        # 获取并从请求参数中剔除signature
        signature = data.pop('sign')

        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 校验这个重定向是否是alipay重定向过来的
        success = alipay.verify(data, signature)
        if success:
            # 读取order_id
            order_id = data.get('out_trade_no')
            # 读取支付宝流水号
            trade_id = data.get('trade_no')
            # 保存Payment模型类数据
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )

            # 修改订单状态为待评价
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])

            # 响应trade_id
            context = {
                'trade_id':trade_id
            }
            return render(request, 'pay_success.html', context)
        else:
            # 订单支付失败，重定向到我的订单
            return http.HttpResponseForbidden('非法请求')
```

> **5.渲染支付成功页面信息**

```html
<div class="common_list_con clearfix">
    <div class="order_success">
        <p><b>订单支付成功</b></p>
        <p>您的订单已成功支付，支付交易号：{{ trade_id }}</p>
        <p><a href="{{ url('orders:info', args=(1, )) }}">您可以在【用户中心】->【我的订单】查看该订单</a></p>
    </div>
</div>
```

<img src="/payment/images/13支付成功.png" style="zoom:50%">

<img src="/payment/images/14显示订单状态为待评价.png" style="zoom:50%">

