"""
/**
 * name: 玩一玩兑换京豆(并发版)
 * desc: 需要兑换的奖品: export JY_JD_WYW_EXCHANGE="120豆&300豆&80豆"
 * cron: 0 0 * * *
 */
"""
import os
import json
import re
import time
from multiprocessing import Pool, Manager
from urllib.parse import unquote

import httpx

from conf import config
from utils.ql import ql
from utils.proxy import get_proxies
from utils.ua import get_jd_ua
from utils.com import match_value_from_cookie


def sleep():
    time.sleep(config.JY_JD_WYW_TIMEOUT)


class JdWywExchange:
    def __init__(self, ck, exchange=config.JY_JD_WYW_EXCHANGE):
        self.ck = ck
        self.pin = unquote(match_value_from_cookie(ck))
        self.client = httpx.Client(
            headers={
                'user-agent': get_jd_ua(),
                'Referer': 'https://pro.m.jd.com/mall/active/3aydrBPrN7xsUGwj31PK3UhkHAqA/index.html?babelChannel',
                'cookie': self.ck,
                'origin': 'https://pro.m.jd.com',
            },
            proxies=get_proxies(),
        )
        self.exchange_list = exchange.split('&')

    def post(self, function_id, body):
        try:
            timestamp = int(time.time() * 1000)
            url = f'https://api.m.jd.com/client.action'
            params = {'functionId': function_id, 'appid': 'signed_wh5', 'client': 'android', 'clientVersion': '13.1.0',
                      'partner': 'jingdong', 't': timestamp, 'osVersion': '14', 'networkType': 'wifi',
                      'x-api-eid-token': '', 'eu': '', 'fv': '', 'openudid': '',
                      'd_brand': 'OnePlus', 'd_model': 'HD1905', 'body': json.dumps(body)}
            response = self.client.post(url, params=params)
            return response.json()
        except Exception as e:
            print(f'请求接口:{function_id}失败, {e.args}')
            return {
                'code': 999,
                'message': '调用失败, 异常!',
                'data': {
                    'bizCode': 999
                }
            }

    def is_exchange(self, reward_name):
        """
        :param reward_name:
        :return:
        """
        r_num, r_unit = re.findall(r'\d+|\D+', reward_name)
        for item in self.exchange_list:
            i_num, i_unit = re.findall(r'\d+|\D+', item)
            if i_num == r_num and i_unit in r_unit:
                return True
        return False

    def print(self, msg):
        print(f'{self.pin}:{msg}')

    def start(self, q):
        data = self.post('wanyiwan_exchange_page', {"version": 3})
        if data.get('code') != 0:
            self.print('获取奖励列表失败, 退出!')
            return

        is_print_reward_info = not q.empty()
        if not q.empty():
            _ = q.get()
        reward_info_msg = ''
        reward_list = data.get('data', {}).get('result', {}).get('moreExchanges', [])
        score = data.get('data', {}).get('result', {}).get('score', 0)
        reward_info_msg += '奖品列表如下(已过滤优惠券):\n======================================\n'
        exchange_list = []
        for reward in reward_list:
            if reward['rewardType'] == 2 or '优惠券' in reward['rewardName']:
                continue

            store_desc = '有库存' if reward['hasStock'] else '无库存'
            reward_info_msg += f'{reward["rewardName"]}({store_desc})|兑换需{reward["exchangeScore"]}奖票!\n'

            if self.is_exchange(reward['rewardName']):
                exchange_list.append(reward)

        reward_info_msg += '======================================'
        if is_print_reward_info:
            print(reward_info_msg)

        exchange_list.sort(key=lambda x: x['exchangeScore'], reverse=True)
        sleep()

        self.print(f'当前有奖票: {score}')
        for exchange in exchange_list:
            if not exchange['hasStock']:
                self.print(f'奖品:《{exchange["rewardName"]}》当前无库存, 不兑换!')
                continue
            if score < exchange['exchangeScore']:
                self.print(f'当前奖票为: {score}, 小于兑换奖票所需{exchange["exchangeScore"]}奖票, 不兑换!')
                continue

            if score - exchange['exchangeScore'] < config.JY_JD_WYW_KEEP_SCORE:
                self.print(f'当前奖票({score}) - 兑换所需奖票({exchange["exchangeScore"]}) = '
                           f'兑换后剩余奖票({score - exchange["exchangeScore"]}) '
                           f' 小于保留奖票({config.JY_JD_WYW_KEEP_SCORE}), 不兑换!')
                continue
            data = self.post('wanyiwan_exchange', {"assignmentId": exchange['assignmentId'],
                                                   "type": exchange['rewardType'], "version": 3})
            if data.get('code') != 0:
                self.print(f'兑换奖品:《{exchange["rewardName"]}》失败, {data["message"]}')
                continue
            if data.get('data').get('bizCode') != 0:
                biz_msg = data.get('data').get('bizMsg')
                self.print(f'兑换奖品:《{exchange["rewardName"]}》失败, {biz_msg}')
                continue

            score -= exchange['exchangeScore']
            self.print(f'兑换奖品:《{exchange["rewardName"]}》成功, 剩余奖票:{score}')
            sleep()


def run(ck, q):
    app = JdWywExchange(ck)
    app.start(q)


if __name__ == '__main__':
    pool = Pool(config.JY_JD_WYW_PROCESS_NUM)
    manager = Manager()
    queue = manager.Queue()
    queue.put('随便啦!')

    if config.BASE_DIR.startswith('/ql'):
        print('当前为青龙本地环境:')
        ck_list = os.environ.get('JD_COOKIE').split('&')
    else:
        ck_list = ql.get_all_jd_ck()
    print(f'总共{len(ck_list)}个JD_COOKIE, 兑换商品:{config.JY_JD_WYW_EXCHANGE}!')
    for ck in ck_list:
        pool.apply_async(run, args=(ck, queue))

    pool.close()
    pool.join()
