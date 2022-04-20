# -*-coding:utf-8-*-
import json
import os
import time
import datetime
import requests
import logger
import database
import config
import urllib3

'''
 * @author dingyanan
 * @date 2022/04/14 15:48
'''
# 微博信息

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/weibo%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)


# 部门服务
def get_name():
    a = database.GetJdStore().getchecck()
    n = 2
    name_list = []
    for r in [a[i:i + n] for i in range(0, len(a), n)]:
        item = {}
        item['name'] = r[0]
        item['mid'] = r[1]
        name_list.append(item)
    return name_list


# 检查僵尸号
def get_weibo():
    name_list = get_name()
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

    for names in name_list:
        item = {}
        item['name'] = names['name']
        item['id'] = id = names['mid']
        url = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={}'.format(
            id, 1)
        try:
            resp = requests.get(url=url, headers=headers,verify=False)
            # resp = requests.get(url=url, headers=headers, proxies=config.proxies, verify=False)
            json_data = resp.content.decode('utf-8')
            json_list = (json.loads(json_data))
            cards_list = (json_list['data']['cards'])
            # 防止置顶微博过期
            for card in cards_list[2:3]:
                try:
                    item['url'] = card['scheme']
                    mblog = card['mblog']
                except Exception as e:
                    logging.info("微博：{},错误".format(len(mblog), e))
                GMT_FORMAT = '%a %b %d %H:%M:%S %Y'
                Time1 = mblog['created_at']
                Time = Time1.replace('+0800 ', '')
                item['pubdate'] = publishtime = datetime.datetime.strptime(Time, GMT_FORMAT)

                # 计算最新微博发布时间距离现在天数，超过60天没更新就是僵尸号
                today = datetime.datetime.today()
                date_count = (today - publishtime).days
                try:
                    if date_count > config.zombie_day:
                        item['is_update'] = 0
                        logging.info('僵尸号：{}，时间为：{},更新距今：{}'.format(item['name'], publishtime, date_count))
                    else:
                        item['is_update'] = 1
                        logging.info('账号：{}，时间为：{},更新距今：{}'.format(item['name'], publishtime, date_count))
                    # database.GetJdStore().is_update(item)
                except Exception as e:
                    logging.info("微博：{}，写入失败,名字:{},错误:{}".format(names, item['name'], e))

        except Exception as e:
            logging.info('请求失败:{}'.format(e))


if __name__ == "__main__":
    get_weibo()
