# celery的入口
from celery import Celery
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery的实例
celery_app = Celery('meiduo')

# 加载配置,在main中告知生产者，中间人是谁。

celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])
