from collections import OrderedDict
from .models import GoodsChannel


def get_breadcrumb(category):
    breadcrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': '',
    }
    if category.parent == None:  # 一级类别展示一级 ，二级类别展示一级，二级，三级类别展示一级，二级，三级
        breadcrumb['cat1'] = category
    elif category.subs.count() == 0:
        # 三级类别展示一级，二级，三级
        breadcrumb['cat3'] = category
        cat2 = category.parent
        breadcrumb['cat2'] = cat2
        cat1 = cat2.parent
        print(cat1.goodschannel_set.all())
        cat1.url = cat1.goodschannel_set.first().url # 取第一个对象的url
        # cat1.url = cat1.goodschannel_set.all()[0].url
        breadcrumb['cat1'] = cat1
    else:
        breadcrumb['cat2'] = category
        breadcrumb['cat1'] = category.parent
    return breadcrumb


def get_categories():
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}
        cat1 = channel.category
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url,
        })

        for cat2 in cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)
    return categories
