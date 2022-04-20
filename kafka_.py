# -*-coding:utf-8-*-kafka_.py
import os
import time

from kafka import KafkaProducer
import logger

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/dbs%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('dbs', log_path)

import config

producer = KafkaProducer(bootstrap_servers=config.SERVER)
topic = config.TOPIC


def kafka(content):
    try:
        f = producer.send(topic, value=str(content).encode('utf-8'))
        f.get(timeout=1)
        # logging.info('新闻数据写入kafka成功,时间为:{}'.format(content['pubdate']))

    except Exception as e:
        logging.info('写入失败，数据回滚：{}'.format(e))


if __name__ == '__main__':
    pass


