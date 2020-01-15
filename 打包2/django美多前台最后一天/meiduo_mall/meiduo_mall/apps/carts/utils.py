import pickle, base64
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    # 合并购物车
    cookie_cart_str = request.COOKIES.get('carts')
    if not cookie_cart_str:
        return response
    cookie_cart_dict = str_to_dict(cookie_cart_str)
    # """
    #  {
    #      11(sku_id): {
    #          "count": "1",
    #          "selected": "True"
    #      },
    #      22: {
    #          "count": "3",
    #          "selected": "True"
    #      },
    #  }
    #  """
    # 准备新的数据容器，保存新的sku_id,selected,unselected
    new_cart_dict = {}
    new_selected_add = []
    new_selected_rem = []
    # 遍历cookie中购物车数据
    for sku_id, cookie_dict in cookie_cart_dict.items():
        # sku_id = 1,2,3
        # cookie_dict = {"count": "3","selected": "True"}
        # 构造成这样：{sku_id:count}     {2:20}
        new_cart_dict[sku_id] = cookie_dict.get('count')
        if cookie_dict['selected']:
            new_selected_add.append(sku_id)
        else:
            new_selected_rem.append(sku_id)
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    pl.hmset('carts_%s' % user.id, new_cart_dict)
    # 将数据同步到redis中
    if new_selected_add:
        pl.sadd('selected_%s' % user.id, *new_selected_add)
    if new_selected_rem:
        pl.srem('selected_%s' % user.id, *new_selected_rem)
    pl.execute()
    response.delete_cookie('carts')
    return response

def str_to_dict(str_data):
    # 'gAN9cQ'
    str_bytes = str_data.encode()
    # b'gAN9cQ'
    dict_bytes = base64.b64decode(str_bytes)
    # b'\x80\x03}q\x00X'
    dict_data = pickle.loads(dict_bytes)
    # dict = {'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}
    return dict_data


def dict_to_str(dict_data):
    # dict = {'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}
    dict_bytes = pickle.dumps(dict_data)
    # b'\x80\x03}q\x00X'
    str_bytes = base64.b64encode(dict_bytes)
    # b'gAN9cQ'
    str_data = str_bytes.decode()
    # 'gAN9cQ'
    return str_data
