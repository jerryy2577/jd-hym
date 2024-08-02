import httpx
import sys
from conf import config
from utils.proxy import get_no_proxies


def get_sign(fn: str, body: str):
    """
    :return:
    """
    if not config.JY_JD_SIGN_URL:
        print('京东签名算法服务配置错误, 请先填写环境变量JY_JD_SIGN_URL="http://xxx.xxx.xxx.xxx:xx"')
        sys.exit(1)

    data = {
        "fn": fn,
        "body": body,
    }
    r = httpx.post(config.JY_JD_SIGN_URL, json=data, proxies=get_no_proxies())
    return r.json()


if __name__ == '__main__':
    print(get_sign(fn='isvObfuscator', body="{\"url\":\"https://lzkj-isv.isvjd.com\",\"id\":\"\"}"))