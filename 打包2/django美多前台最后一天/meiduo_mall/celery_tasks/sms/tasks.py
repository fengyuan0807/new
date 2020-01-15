# 定义任务
from celery_tasks.sms.yuntongxun.ccp_sms import CCP
from celery_tasks.sms import constants
from celery_tasks.main import celery_app
import logging

logger = logging.getLogger('django')

@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self,mobile, sms_code):
    """发送短信验证码的异步任务"""
    try:

        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                           constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        logger.error(e)
        raise self.retry(exc=e, max_retries=3)

