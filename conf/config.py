import os
import shutil

from dotenv import dotenv_values
from collections import OrderedDict


class Config:
    # 项目根目录
    BASE_DIR = ''
    # 缓存目录
    CACHE_DIR = ''
    # 日志目录
    LOG_DIR = ''
    # 青龙URL
    JY_QL_URL: str = ''
    # 青龙Client Id
    JY_QL_CLIENT_ID: str = ''
    # 青龙Client secret
    JY_QL_CLIENT_SECRET: str = ''
    # jd h5st算法url
    JY_JD_H5ST_URL: str = ''
    # jd sign签名算法url
    JY_JD_SIGN_URL: str = ''
    # 代理池URL
    JY_PROXY_POOL_URL: str = ''
    # TG机器人
    JY_TG_BOT_TOKEN: str = ''
    # TG群ID
    JY_TG_GROUP_ID: str = ''

    # Redis配置
    JY_REDIS_HOST: str = '127.0.0.1'
    JY_REDIS_PORT: int = 6379
    JY_REDIS_DB: int = 8

    # TG Api
    JY_TG_API_ID: str = ''
    JY_TG_API_HASH: str = ''
    JY_TG_RECEIVER_LINK = ''
    JY_TG_SESSION_PATH = ''
    JY_ACT_TIMEOUT = 5

    # 京东活动搜索关键词
    JY_JD_ACT_KEYWORD = ''

    # 兑换商品
    JY_JD_WYW_EXCHANGE = '300豆&120豆&80豆'
    # 玩一玩保留奖票
    JY_JD_WYW_KEEP_SCORE = 200

    # 玩一玩请求间隔
    JY_JD_WYW_TIMEOUT = 1
    
    # 玩一玩进程数量
    JY_JD_WYW_PROCESS_NUM = 4

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if value.isdigit():
                    value = int(value)
                setattr(self, key, value)


def find_project_root():
    """
    查找项目根目录
    :return:
    """
    current_path = os.getcwd()
    while current_path != os.path.dirname(current_path):
        if '.git' in os.listdir(current_path) or '.env' in os.listdir(current_path) or 'jd_scan_act.py' in os.listdir(
                current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    return None


def load_dotenv(base_dir):
    env_path = os.path.join(base_dir, '.env')
    env_example_path = os.path.join(base_dir, '.env.example')
    if not os.path.exists(env_path):
        shutil.copy(env_example_path, env_path)
    values = dotenv_values(env_path)
    return values


config = Config()
# 项目根目录
BASE_DIR = find_project_root()
config.set(BASE_DIR=BASE_DIR)

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'storage', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
config.set(LOG_DIR=LOG_DIR)

# 缓存目录
CACHE_DIR = os.path.join(BASE_DIR, 'storage', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)
config.set(CACHE_DIR=CACHE_DIR)

# TG Session缓存路径
config.set(JY_TG_SESSION_PATH=os.path.join(CACHE_DIR, 'tg.session'))

config.set(**load_dotenv(BASE_DIR))

if __name__ == '__main__':
    print(config.BASE_DIR)
    print(config.JY_QL_URL)
