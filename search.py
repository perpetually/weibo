# -*-coding:utf-8-*-

import json
import os
import random
import re
import time
import requests
import config
import logger
import database

import urllib3

'''
 * @author dingyanan
 * @date 2021/10/21 15:48
'''
# 微博信息

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/weibo%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)


# 目标url
def get_weibo():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'referer': 'https://m.weibo.cn/sw.js',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36'
    }

    pages = 4
    user_name = {}
    for page in range(1, pages):
        name = '发布'
        url = 'https://m.weibo.cn/api/container/getIndex?'
        params = {'containerid': '100103type=3&q={}&t=0'.format(name),
                  'title': '机构认证-{}'.format(name),
                  'extparam': 'q={}&isv=3&specfilter=1&log_type=6&lfid_type=39'.format(name),
                  'luicode': '10000011',
                  'lfid': '100103type=39&q={}&t=0'.format(name),
                  'page': page,
                  }
        try:
            # resp = requests.get(url=url, headers=headers, params=params,proxies=config.proxies, verify=False)
            resp = requests.get(url=url, headers=headers, params=params,  verify=False)
            json_data = resp.content.decode('utf-8')
            json_list = (json.loads(json_data))
            card_group = json_list['data']['cards'][0]['card_group']
            item = {}
            for card in card_group:
                item['url'] = card['scheme']
                item['mid'] = str(107603) + str(card['user']['id'])
                item['name'] = card['user']['screen_name']
                item['follow'] = card['user']['follow_count']
                item['fans'] = card['user']['followers_count']
                item['description'] = card['user']['description']
                user_name[item['name']] = item['mid']
                # database.GetJdStore().weibo_source(item)
                logging.info('当前页码：{}。用户信息为：{}'.format(page, item['name']))

        except Exception as e:
            logging.info('请求失败:{}'.format(e))

    logging.info('所有urse_name为：{}'.format(user_name))


if __name__ == "__main__":
    get_weibo()
