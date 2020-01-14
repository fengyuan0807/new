# 展示提交订单成功页面

> 支付方式：货到付款

<img src="/orders/images/05提交订单成功2.png" style="zoom:40%">

> 支付方式：支付宝

<img src="/orders/images/05提交订单成功1.png" style="zoom:40%">

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /orders/success/ |

> **2.请求参数：**

```
无
```

> **3.响应结果：HTML**

```
order_success.html
```

> **4.后端接口定义和实现**

```python
class OrderSuccessView(LoginRequiredMixin, View):
    """提交订单成功"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        context = {
            'order_id':order_id,
            'payment_amount':payment_amount,
            'pay_method':pay_method
        }
        return render(request, 'order_success.html', context)
```

> **5.渲染提交订单成功页面信息**

```html
<div class="common_list_con clearfix">
    <div class="order_success">
        <p><b>订单提交成功，订单总价<em>¥{{ payment_amount }}</em></b></p>
        <p>您的订单已成功生成，选择您想要的支付方式，订单号：{{ order_id }}</p>
        <p><a href="{{ url('orders:info', args=(1, )) }}">您可以在【用户中心】->【我的订单】查看该订单</a></p>
    </div>
</div>
<div class="order_submit clearfix">
    {% if pay_method == '1' %}
        <a href="{{ url('contents:index') }}">继续购物</a>
    {% else %}
        <a @click="order_payment" class="payment">去支付</a>
    {% endif %}
</div>
```