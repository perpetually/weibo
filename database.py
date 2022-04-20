# coding=utf-8
import os
import time
from itertools import chain
import pymysql, json
import logger
import config

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/weibo%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('weibo', log_path)


class GetJdStore:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            passwd=config.passwd,
            database=config.database,
            charset=config.charset
        )

    #   微博舆情
    def weibo_news(self, item):
        url = item['url']
        content = item['content']
        reposts_count = item['reposts_count']
        comments_count = item['comments_count']
        attitudes_count = item['attitudes_count']
        data_id = item['mid']
        publish_time = str(item['publish_time'])
        forward_content = item['forward_text']
        name = item['name']
        source = item['source']
        images = json.dumps(item['images'])
        type = item['type']
        level = item['level']

        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句

        sql = "INSERT INTO {}(url,content,reposts_count, comments_count, attitudes_count, data_id, publish_time,forward_content,name, source,images,type,level) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE content = VALUES(content), update_time = CURRENT_TIMESTAMP ".format('weibo2')

        try:
            # 执行sql语句
            cursor.execute(sql, [url, content, reposts_count, comments_count, attitudes_count, data_id, publish_time,
                                 forward_content, name, source, images, type, level])
            # 提交到数据库执行
            self.db.commit()
            # logging.info("微博写入成功,标题为:{},时间为：{}".format(name, pubdate))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    # 第一版，已经不用了
    def weibo(self, item):
        url = item['url']
        text = item['text']
        reposts_count = item['reposts_count']
        comments_count = item['comments_count']
        attitudes_count = item['attitudes_count']
        mid = item['mid']
        pubdate = item['pubdate']
        forward_text = item['forward_text']
        name = item['name']
        source = item['source']
        images = json.dumps(item['images'])
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句

        sql = "INSERT INTO weibo(url,text,reposts_count,comments_count,attitudes_count,mid,pubdate,forward_text,name, source,images) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE images = VALUES(images), update_time = CURRENT_TIMESTAMP "

        try:
            # 执行sql语句
            cursor.execute(sql,
                           [url, text, reposts_count, comments_count, attitudes_count, mid, pubdate, forward_text, name,
                            source, images])
            # 提交到数据库执行
            self.db.commit()
            # logging.info("微博写入成功,标题为:{},时间为：{}".format(name, pubdate))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    # 微博个人主页
    def weibo_source(self, item):
        # 使用cursor()方法获取操作游标
        url = item['url']
        mid = item['mid']
        name = item['name']
        follow = item['follow']
        fans = item['fans']
        description = item['description']
        cursor = self.db.cursor()

        sql = "INSERT INTO weibo_source(url, mid, name, follow,fans,description) " \
              "VALUES (%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE name = VALUES(name), update_time = CURRENT_TIMESTAMP "
        try:
            # 执行sql语句
            cursor.execute(sql, [url, mid, name, follow, fans, description])
            # 提交到数据库执行
            self.db.commit()
            logging.info("数据写入成功,标题为:{}".format(name))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    # 僵尸号检测
    def is_update(self, item):
        # 使用cursor()方法获取操作游标

        mid = item['id']
        is_update = item['is_update']
        cursor = self.db.cursor()

        sql = "INSERT INTO weibo_source(mid,is_update) " \
              "VALUES (%s,%s)ON DUPLICATE KEY " \
              "UPDATE is_update = VALUES(is_update), update_time = CURRENT_TIMESTAMP "
        try:
            # 执行sql语句
            cursor.execute(sql, [mid, is_update])
            # 提交到数据库执行
            self.db.commit()
            logging.info("数据写入成功,账号为:{}".format(mid))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    def getSearch(self):
        cur = self.db.cursor()
        # 查询
        sql = "select name , mid from weibo_source where is_update =1"
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            resultlist = list(chain.from_iterable(results))
            return resultlist

        except Exception as e:

            logging.info("查询错误{}".format(e))
            raise e
        finally:
            self.db.close()  # 关闭连接

    def getchecck(self):
        cur = self.db.cursor()
        # 查询
        sql = "select name , mid from weibo_source where is_update is null"
        # sql = "select name , mid from weibo_source"
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            resultlist = list(chain.from_iterable(results))
            return resultlist

        except Exception as e:

            logging.info("查询错误{}".format(e))
            raise e
        finally:
            self.db.close()  # 关闭连接


if __name__ == '__main__':
    pass
