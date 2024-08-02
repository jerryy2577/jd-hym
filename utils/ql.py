import random
import sys

import httpx

from conf import config
from utils.proxy import get_no_proxies


class Ql:
    def __init__(self, ql_url, ql_client_id, ql_client_secret):
        if not ql_url.startswith('http'):
            print('QL_URL环境变量配置错误, 请检查配置!')
            sys.exit(1)

        self.ql_url = ql_url
        self.ql_client_id = ql_client_id
        self.ql_client_secret = ql_client_secret
        self.token = ''
        self.client = httpx.Client(base_url=f'{self.ql_url}/open', proxies=get_no_proxies())

        auth_data = self.authenticate()
        if not auth_data:
            print('未能成功获取青龙授权, 退出程序!')
            sys.exit(1)

        self.client.headers.update({"authorization": auth_data.get('token_type') + ' ' + auth_data.get('token')})

    def authenticate(self):
        try:
            params = {
                'client_id': self.ql_client_id,
                'client_secret': self.ql_client_secret,
            }
            r = self.client.get(f'/auth/token', params=params)
            data = r.json()
            if data.get('code') == 200:
                return data['data']
            else:
                print('获取青龙token失败, 请检测青龙相关配置是否正确!')
                return {}
        except Exception as e:
            print('获取青龙授权token失败, 请检查青龙相关配置是否正确!错误信息:{}'.format(e.args))
            return {}

    def get_all_envs(self):
        """
        :return:
        """
        r = self.client.get(f'/envs')
        return r.json().get('data', [])

    def get_env_by_id(self, env_id):
        r = self.client.get(f'/envs/{env_id}')
        return r.json().get('data', None)

    def get_random_jd_ck(self):
        """
        随机返回一个CK
        :return:
        """
        envs = self.get_all_envs()
        if not envs:
            return None

        ck_list = []
        for env in envs:
            if 'pt_key=' in env['value'] and env['status'] == 0:
                ck_list.append(env['value'])

        if not ck_list:
            return None

        return random.choice(ck_list)

    def get_all_jd_ck(self):
        ck_list = []
        envs = self.get_all_envs()
        if not envs:
            return ck_list

        for env in envs:
            if 'pt_key=' in env['value'] and env['status'] == 0:
                ck_list.append(env['value'])

        return ck_list


ql = Ql(config.JY_QL_URL, config.JY_QL_CLIENT_ID, config.JY_QL_CLIENT_SECRET)


if __name__ == '__main__':
    print(ql.get_random_jd_ck())
