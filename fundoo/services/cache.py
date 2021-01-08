import redis
from decouple import config


class Cache:
    """
    this class is used to set and get cache from redis
    """

    def __init__(self):
        """
        this method creates a connection with redis server
        """
        self.r = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))

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
