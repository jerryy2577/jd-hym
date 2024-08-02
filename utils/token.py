import json
from hashlib import md5

import httpx
from utils.proxy import get_proxies
from utils.sign import get_sign
from utils.db import redis_conn
from utils.com import match_value_from_cookie

token_cache_prefix = 'jd_isv_token:'


def get_isv_token_from_api(cookie):
    """
    :param cookie:
    :return:
    """
    headers = {
        'user-agent': 'okhttp/3.12.16;jdmall;android;version/13.1.0;build/99208;',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
    }
    resp = get_sign('isvObfuscator', json.dumps({"id": "", "url": "https://lzkj-isv.isvjd.com/"}))
    url = 'https://api.m.jd.com/client.action?functionId=isvObfuscator&' + resp['body']
    response = httpx.post(url, headers=headers, proxies=get_proxies())
    return response.json().get('token', None)


def get_isv_token(cookie):

    pt_pin_md5 = md5(match_value_from_cookie(cookie).encode('utf-8')).hexdigest()
    cache_key = f'{token_cache_prefix}_{pt_pin_md5}'

    token = redis_conn().get(cache_key)
    if token:
        print(f'从缓存中读取到Token:{token.decode("utf-8")}')
        return token.decode('utf-8')

    token = get_isv_token_from_api(cookie)

    if not token:
        print('缓存中无Token, 并且API获取Token失败!')
        return None

    if token:
        print('从API中获取Token, 缓存Token')
        redis_conn().set(cache_key, token, 29 * 60)

    return token










