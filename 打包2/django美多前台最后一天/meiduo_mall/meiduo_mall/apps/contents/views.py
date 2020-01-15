from collections import OrderedDict

from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views import View

from goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory
from contents.models import Content, ContentCategory
from goods.utils import get_categories


# Create your views here.

class IndexView(View):
    def get(self, request):
        # 提供首页广告页面

        # {
        #     "1":{
        #         "channels":[
        #             {"id":1, "name":"手机", "url":"http://shouji.jd.com/"},
        #             {"id":2, "name":"相机", "url":"http://www.itcast.cn/"},
        #             {"id":3, "name":"数码", "url":"http://www.itcast.cn/"},
        #         ],
        #         "sub_cats":[
        #             {
        #                 "id":38,
        #                 "name":"手机通讯",
        #                 "sub_cats":[
        #                     {"id":115, "name":"手机"},
        #                     {"id":116, "name":"游戏手机"}
        #                 ]
        #             },
        #             {
        #                 "id":39,
        #                 "name":"手机配件",
        #                 "sub_cats":[
        #                     {"id":119, "name":"手机壳"},
        #                     {"id":120, "name":"贴膜"}
        #                 ]
        #             }
        #         ]
        #     }
        # }
        # 查询并展示所有的分类
        # GoodsChannelGroup -->GoodsChannel -->GoodsCategory
        # 一对多,从频道开始查找
        # 查询所有的频道37个
        # channels = GoodsChannel.objects.all().order_by('group_id', 'sequence')
        # categories = OrderedDict()
        # # 遍历所有的频道
        # for channel in channels:
        #     # 由后端渲染jinja2引擎
        #     # 这个频道属于哪个组的
        #     group_id = channel.group_id  # 当前的频道所属的组 多查一
        #     if group_id not in categories:  # 如果key不存在，那么新建key:value
        #         categories[group_id] = {'channels': [], 'sub_cats': []}
        #     # 当前频道的类别
        #     cat1 = channel.category
        #     categories[group_id]['channels'].append({
        #         'id': cat1.id,
        #         'name': cat1.name,
        #         'url': channel.url
        #     })
        #     cat2s = cat1.subs.all()
        #     for cat2 in cat2s:
        #         sub_cats=[]
        #         categories[group_id]['sub_cats'].append({
        #             'id':cat2.id,
        #             'name':cat2.name,
        #             "sub_cats":sub_cats
        #         })
        #
        #         for cat3 in cat2.subs.all():
        #             sub_cats.append(cat3)
        # for channel in channels:
        #     group_id = channel.group_id
        #     if group_id not in categories:
        #         categories[group_id] = {'channels': [], 'sub_cats': []}
        #     cat1 = channel.category
        #     categories[group_id]['channels'].append({
        #         'id': cat1.id,
        #         'name': cat1.name,
        #         'url': channel.url,
        #     })
        #
        #     for cat2 in cat1.subs.all():
        #         cat2.sub_cats = []
        #         for cat3 in cat2.subs.all():
        #             cat2.sub_cats.append(cat3)
        #         categories[group_id]['sub_cats'].append(cat2)
        categories = get_categories()
        # 展示首页广告
        # {
        #     "index_lbt": [
        #         {
        #             "title": "美图M8s",
        #             "url": "http://www.itcast.cn",
        #             "image": "group1/M00/00/01/CtM3BVrLmc-AJdVSAAEI5Wm7zaw8639396",
        #             "text": ""
        #         },
        #         {
        #             "title": "黑色星期五",
        #             "url": "http://www.itcast.cn",
        #             "image": "group1/M00/00/01/CtM3BVrLmiKANEeLAAFfMRWFbY86177278",
        #             "text": ""
        #         },
        #         {
        #             "title": "厨卫365",
        #             "url": "http://www.itcast.cn",
        #             "image": "group1/M00/00/01/CtM3BVrLmkaAPIMJAAESCG7GAh43642702",
        #             "text": ""
        #         },
        #         {
        #             "title": "君乐宝买一送一",
        #             "url": "http://www.itcast.cn",
        #             "image": "group1/M00/00/01/CtM3BVrLmnaADtSKAAGlxZuk7uk4998927",
        #             "text": ""
        #         }
        #     ],
        # }
        # content ={}
        # content_categories = ContentCategory.objects.all()
        # for content_categorie in content_categories:
        #     # 一对多
        #     content_categorie.content_set.filter
        contents = OrderedDict()
        # 查询所有的广告类别
        content_categories = ContentCategory.objects.all()
        for content_categorie in content_categories:
            # {cat.key:[{},{},{}]}
            contents[content_categorie.key] = content_categorie.content_set.filter(status=True).order_by('sequence')
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)

