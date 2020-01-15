from datetime import datetime

from django.utils import timezone

import os
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
  # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_demo.settings')
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev") # 如果更改了setting的位置 写成这样

# 让Django进行一次初始化
import django
django.setup()

t = timezone.now()
print(t)
print(type(t))
t1=timezone.localtime()
print(t1)
today_str = '%d-%02d-%02d' % (t1.year, t1.month, t1.day)
# print(today_str)
# print(type(today_str))
today_date = datetime.strptime(today_str, '%Y-%m-%d')
print(today_date)
print(type(today_date))

t1 = t.strftime('%Y%m%d%H%M%S')
print(t1)