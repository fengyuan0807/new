# 使用乐观锁并发下单

> **重要提示：**

* 在多个用户同时发起对同一个商品的下单请求时，先查询商品库存，再修改商品库存，会出现资源竞争问题，导致库存的最终结果出现异常。

### 1. 并发下单问题演示和解决方案

<img src="/orders/images/04并发下单问题演示.png" style="zoom:50%">

> **解决办法：**

* 悲观锁
    * 当查询某条记录时，即让数据库为该记录加锁，锁住记录后别人无法操作，使用类似如下语法
    ```python
    select stock from tb_sku where id=1 for update;
    
    SKU.objects.select_for_update().get(id=1)
    ```
    * 悲观锁类似于我们在多线程资源竞争时添加的互斥锁，容易出现死锁现象，采用不多。

* 乐观锁
    * 乐观锁并不是真实存在的锁，而是在更新的时候判断此时的库存是否是之前查询出的库存，如果相同，表示没人修改，可以更新库存，否则表示别人抢过资源，不再执行库存更新。类似如下操作
    ```python
    update tb_sku set stock=2 where id=1 and stock=7;
    
    SKU.objects.filter(id=1, stock=7).update(stock=2)
    ```
* 任务队列
    * 将下单的逻辑放到任务队列中（如celery），将并行转为串行，所有人排队下单。比如开启只有一个进程的Celery，一个订单一个订单的处理。

### 2. 使用乐观锁并发下单

> 思考：
* 下单成功的条件是什么？
    * 首先库存大于购买量，然后更新库存和销量时原始库存没变。

> 结论：
* 所以在用户库存满足的情况下，如果更新库存和销量时原始库存有变，那么继续给用户下单的机会。

```python
class OrderCommitView(LoginRequiredJSONMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前保存订单时需要的信息
        ......

        # 显式的开启一个事务
        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()

            # 暴力回滚
            try:
                # 保存订单基本信息 OrderInfo（一）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                # 从redis读取购物车中被勾选的商品信息
                redis_conn = get_redis_connection('carts')
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)
                selected = redis_conn.smembers('selected_%s' % user.id)
                carts = {}
                for sku_id in selected:
                    carts[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = carts.keys()

                # 遍历购物车中被勾选的商品信息
                for sku_id in sku_ids:
                    while True:
                        # 查询SKU信息
                        sku = SKU.objects.get(id=sku_id)

                        # 读取原始库存
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        # 判断SKU库存
                        sku_count = carts[sku.id]
                        if sku_count > origin_stock:
                            # 事务回滚
                            transaction.savepoint_rollback(save_id)
                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                        # 模拟延迟
                        # import time
                        # time.sleep(5)

                        # SKU减少库存，增加销量
                        # sku.stock -= sku_count
                        # sku.sales += sku_count
                        # sku.save()

                        # 乐观锁更新库存和销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                        # 如果下单失败，但是库存足够时，继续下单，直到下单成功或者库存不足为止
                        if result == 0:
                            continue

                        # 修改SPU销量
                        sku.spu.sales += sku_count
                        sku.spu.save()

                        # 保存订单商品信息 OrderGoods（多）
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price,
                        )

                        # 保存商品订单中总价和总数量
                        order.total_count += sku_count
                        order.total_amount += (sku_count * sku.price)

                        # 下单成功或者失败就跳出循环
                        break

                # 添加邮费和保存订单信息
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                # 事务回滚
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})

        # 保存订单数据成功，显式的提交一次事务
        transaction.savepoint_commit(save_id)

        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('carts_%s' % user.id, *selected)
        pl.srem('selected_%s' % user.id, *selected)
        pl.execute()

        # 响应提交订单结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})
```

### 3. MySQL事务隔离级别

* 事务隔离级别指的是在处理同一个数据的多个事务中，一个事务修改数据后，其他事务何时能看到修改后的结果。

* MySQL数据库事务隔离级别主要有四种：
    * `Serializable`：串行化，一个事务一个事务的执行。
    * `Repeatable read`：可重复读，无论其他事务是否修改并提交了数据，在这个事务中看到的数据值始终不受其他事务影响。
    * `Read committed`：读取已提交，其他事务提交了对数据的修改后，本事务就能读取到修改后的数据值。
    * `Read uncommitted`：读取未提交，其他事务只要修改了数据，即使未提交，本事务也能看到修改后的数据值。
    * MySQL数据库默认使用可重复读（ Repeatable read）。

* 使用乐观锁的时候，如果一个事务修改了库存并提交了事务，那其他的事务应该可以读取到修改后的数据值，所以不能使用可重复读的隔离级别，应该修改为读取已提交（Read committed）。

* 修改方式：

<img src="/orders/images/03修改事务隔离级别1.png" style="zoom:50%">

<img src="/orders/images/03修改事务隔离级别2.png" style="zoom:50%">





