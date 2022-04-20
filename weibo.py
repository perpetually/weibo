# -*-coding:utf-8-*-
import hashlib
import json
import os
import random
import re
import time
import datetime
import redis
import requests

# import kafka_
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

try:
    # 获取cookie
    cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
    wechat_md5 = cookie_pool.smembers(config.wechat_md5)
except Exception as e:
    logging.info("redis请求cookie失败,重新请求:{}".format(e))


# 部门服务
def get_name():
    a = database.GetJdStore().getSearch()
    n = 2
    name_list = []
    for r in [a[i:i + n] for i in range(0, len(a), n)]:
        item = {}
        item['name'] = r[0]
        item['mid'] = r[1]
        name_list.append(item)
    return name_list


# 目标url
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

    pages = 2
    for page in range(1, pages):
        for names in name_list:
            item = {}
            item['name'] = names['name']
            item['id'] = id = names['mid']
            url = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={}'.format(
                id, page)
            try:
                # resp = requests.get(url=url, headers=headers, proxies=config.proxies, verify=False)
                resp = requests.get(url=url, headers=headers, verify=False)
                json_data = resp.content.decode('utf-8')
                json_list = (json.loads(json_data))
                cards_list = (json_list['data']['cards'])
                for card in cards_list[:5]:
                    try:
                        item['url'] = card['scheme']
                        mblog = card['mblog']
                    except Exception as e:
                        logging.info("微博：{},错误".format(len(mblog), e))

                    md5_news = hashlib.md5(item['url'].encode('utf-8')).hexdigest().encode('utf-8')
                    if md5_news in wechat_md5:
                        logging.info('数据重复：{}'.format(item['name']))
                    else:
                        cookie_pool.sadd(config.wechat_md5, md5_news)
                        # 点赞，评论，转发,来源,唯一id
                        item['reposts_count'] = mblog['reposts_count']
                        item['comments_count'] = mblog['comments_count']
                        item['attitudes_count'] = mblog['attitudes_count']
                        item['name'] = mblog['user']['screen_name']
                        item['source'] = mblog['source']
                        item['mid'] = mblog['mid']
                        item['gather_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S"))
                        item['type'] = 3
                        item['level'] = 2

                        # 微博详情
                        try:
                            resp = requests.get(url=item['url'], headers=headers)
                            html = resp.text
                            item['content'] = ''.join(re.findall('"text": (.*?",)', html))
                        except Exception as e:
                            logging.info('请求失败：{}'.format(e))

                        GMT_FORMAT = '%a %b %d %H:%M:%S %Y'
                        Time1 = mblog['created_at']
                        Time = Time1.replace('+0800 ', '')
                        item['publish_time'] = datetime.datetime.strptime(Time, GMT_FORMAT)
                        item['forward_text'] = ''
                        item['images'] = ''
                        images = mblog.get('pics')

                        if images:
                            img_list = []
                            for img in images:
                                imgs = img['url']
                                img_list.append(imgs)
                            item['images'] = img_list

                        # 转发内容
                        if 'retweeted_status' in mblog:
                            item['forward_content'] = mblog['retweeted_status']['text']

                        try:
                            # kafka_.kafka(item)
                            # database.GetJdStore().weibo_news(item)
                            logging.info('微博:{},时间:{}'.format(item['name'], item['publish_time']))
                        except Exception as e:
                            logging.info("微博：{}，写入失败,名字:{},错误:{}".format(item['name'], item['publish_time'], e))

            except Exception as e:
                logging.info('请求失败:{}'.format(e))


if __name__ == "__main__":
    get_weibo()
