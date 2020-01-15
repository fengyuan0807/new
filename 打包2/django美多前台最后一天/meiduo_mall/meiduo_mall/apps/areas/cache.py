from django_redis import get_redis_connection


class Cacahe(object):
    def __init__(self, key, value, time, redis_conn):
        self.key = key
        self.value = value
        self.time = time
        self.redis_conn = get_redis_connection('default')

    def __set__(self):
        return self.redis.conn.setex(self.key, self.value, self.time, )

    def __get__(self):
        return self.redis_conn.get(self.key)

    def __del__(self):
        return self.redis.conn.delete(self.key)


cache = Cacahe()

