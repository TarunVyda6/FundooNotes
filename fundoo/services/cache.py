import redis
from decouple import config


class Cache:
    """
    this class is used to set and get cache from redis
    """

    __instance__ = None

    def __init__(self, host, port):
        """
        this method creates a connection with redis server
        """
        self.r = redis.StrictRedis(host=host, port=port)

    @staticmethod
    def get_instance():
        """
        this method will check wheather the instance is already created or not, if instance not created then it will
        create instance and return instance
        """
        if not Cache.__instance__:
            Cache.__instance__ = Cache(config('REDIS_HOST'), config('REDIS_PORT'))
        return Cache.__instance__

    def set_cache(self, key, value):
        """
        it takes key and value value as inputs and stores it in redis server and has expiry time of 1500 seconds
        """
        self.r.set(key, value)
        self.r.expire(key, time=1500)

    def get_cache(self, key):
        """
        it takes key as input and returns value stored with that key
        """
        return self.r.get(key)

    def delete_cache(self, key):
        """
        it takes key as input and delete value stored with that key in redis
        """
        self.r.delete(key)
