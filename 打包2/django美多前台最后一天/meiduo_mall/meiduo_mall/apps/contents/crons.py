# 封装首页静态化过程
import os
from collections import OrderedDict

import time
from django.template import loader
from django.conf import settings

from contents.models import ContentCategory
from goods.utils import get_categories


def generate_static_index_html():
    print('%s: generate_static_index_html' % time.ctime())
    categories = get_categories()
    # 展示首页广告
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
    # 获取首页模板文件
    template = loader.get_template('index.html')
    # 渲染首页html字符串
    html_text = template.render(context)
    # 将首页html字符串写入到static文件夹中 命名为‘index.html’
    # STATICFILES_DIRS: ['/home/python/Desktop/project/meiduo_project/meiduo_mall/meiduo_mall/static']
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html') # 文件的位置
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
