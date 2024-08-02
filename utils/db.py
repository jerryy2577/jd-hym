import redis
from conf import config
from redisbloom.client import Client

pool = redis.ConnectionPool(host=config.JY_REDIS_HOST, port=config.JY_REDIS_PORT, db=config.JY_REDIS_DB)

bf_name = 'activity_bloom'


def redis_conn():
    return redis.Redis(connection_pool=pool)


def rb():
    return Client(connection_pool=pool)


def rb_add(url):
    """
    :param url:
    :return:
    """
    rb().bfAdd(bf_name, url)


def rb_exists(url):
    return rb().bfExists(bf_name, url)


if __name__ == '__main__':
    redis_conn().set('key', '123', 10)
    print(redis_conn().get('key'))
