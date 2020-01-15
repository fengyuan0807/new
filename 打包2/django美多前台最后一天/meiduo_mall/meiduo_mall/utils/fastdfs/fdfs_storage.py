from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.exceptions import APIException


class FdfsStorage(Storage):
    """FDFS自定义文件存储类"""

    def __init__(self, client_conf=None, base_url=None):
        # 保存客户端配置文件路径
        self.base_conf = client_conf or settings.FDFS_CLIENT_CONF
        # # FDFS nginx的地址
        self.base_url = base_url or settings.FDFS_BASE_URL
        # if client_conf is None:
        #     client_conf = settings.FDFS_CLIENT_CONF
        #
        # self.client_conf = client_conf
        #
        # if base_url is None:
        #     base_url = settings.FDFS_URL
        #
        # self.base_url = base_url

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        """
           name: 上传文件的名称
           content: 包含上传文件内容的File对象，content.read()获取上传文件内容
        """
        # 'fdfs客户端配置文件路径'
        client = Fdfs_client(self.base_conf)
        # 上传文件到FDFS系统
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise APIException('上传文件到FDFS系统失败')
        # 获取返回的文件id
        file_id = res.get('Remote file_id')
        return file_id

    def exists(self, name):
        """
              判断上传文件的名称和文件系统中原有的文件名是否冲突
              name: 上传文件的名称
              """
        return False

    def url(self, name):
        # return settings.FDFS_BASE_URL + name
        return self.base_url + name
