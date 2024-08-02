"""
/**
 * name: 超级互动程序扫描活动
 * cron: */30 * * * *
 */
"""

import time
import httpx
from urllib.parse import quote
from conf import config
from utils.com import get_timestamp_n_days_ago
from utils.proxy import get_proxies
from utils.token import get_isv_token
from utils.tg import send_msg_to_tg
from utils.db import rb_exists, rb_add
from utils.ql import ql


class StoreActivity:

    def __init__(self, cookie):
        base_url = ('https://lzkj-isv.isvjd.com/wxAssemblePage/activity/67dfd244aacb438893a73a03785a48c7&ID'
                    '=6ffd61ca1a924f9989e44b7ea9216ee8')
        self.base_url = base_url
        self.client = httpx.Client(verify=False, proxies=get_proxies(), timeout=20)
        self.client.headers.update({
            'Referer': self.base_url,
        })
        self.token = get_isv_token(cookie)

        self.secret_pin = ''

        if not self.token:
            print('获取Token失败, 退出!')
            return

    def jump_to_activity(self):
        """
        跳转活动
        :return:
        """
        to_url = quote(self.base_url)
        url = f'https://un.m.jd.com/cgi-bin/app/appjmp?tokenKey={self.token}&sceneid=25&to={to_url}'
        res = self.client.get(url, follow_redirects=True)
        if res.cookies.get('LZ_TOKEN_VALUE', None):
            return True
        return False

    def get_today_new_activity(self):
        """
        获取今日上新活动列表
        :return:
        """
        try:
            url = 'https://lzkj-isv.isvjd.com/wxAssemblePage/getTopAndNewActInfo'
            params = {
                'pin': self.secret_pin,
                'aggrateActType': 0,
                'topNewType': 2,
                'pageNo': 1,
                'pageSize': 100
            }
            response = self.client.post(url, data=params)
            data = response.json()
            return data.get('data', {}).get('homeInfoResultVOList', [])
        except Exception as e:
            print(f'获取<今日上新>活动列表失败, {e.args}')
            return []

    def get_keyword_activity_list(self, keyword='酒'):
        """
        :return:
        """
        try:
            self.client.headers.update({
                'Referer': 'https://lzkj-isv.isvjd.com/wxAssemblePage/queryActInfo'
            })
            params = {
                "pin": self.secret_pin,
                "pageNo": 1,
                "pageSize": 100000,
                "name": keyword
            }
            url = 'https://lzkj-isv.isvjd.com/wxAssemblePage/queryActInfo'
            response = self.client.post(url, data=params)
            data = response.json()
            return data.get('data', {}).get('homeInfoResultVOList', [])
        except Exception as e:
            print(f'搜索关键词:<{keyword}>活动失败, {e.args}')
            return []

    @staticmethod
    def process(activity_list):
        skip_num = 0
        act_list = []
        for act in activity_list:
            if not act:
                continue
            update_time = act.get('updateTime')
            if get_timestamp_n_days_ago(1) < update_time < int(time.time() * 1000):
                skip_num += 1
                continue
            act_url = act.get('activityUrl')
            if rb_exists(act_url):
                continue

            act_name = act.get('activityTitle')
            shop_name = act.get('shopName')

            rb_add(act_url)
            act_list.append(f'{shop_name}->{act_name}: \n{act_url}')

        print(f'已过滤活动:{skip_num}个, 有效活动:{len(act_list)}个!')
        for act in act_list:
            print(act)
            send_msg_to_tg(act)

    def start(self):
        if not self.jump_to_activity():
            print('跳转登录失败, 退出!')
            return

        print('正在获取今日上新活动列表:')
        act_list = self.get_keyword_activity_list()
        self.process(act_list)

        time.sleep(config.JY_ACT_TIMEOUT)

        keyword_list = config.JY_JD_ACT_KEYWORD.split(',')
        for keyword in keyword_list:
            print(f'正在搜索关键词:<{keyword}>活动列表:')
            act_list = self.get_keyword_activity_list(keyword)
            self.process(act_list)
            time.sleep(config.JY_ACT_TIMEOUT)


if __name__ == '__main__':
    app = StoreActivity(ql.get_random_jd_ck())
    app.start()

