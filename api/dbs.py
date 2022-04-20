# coding=utf-8
from itertools import chain
import pymysql
import config

class Tea:
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

    def weibo(self, pagesize, page):
        cur = self.db.cursor()

        sql = "SELECT url,content,reposts_count, comments_count, attitudes_count, data_id, publish_time,forward_content,name, source,images,type,level,create_time,(SELECT count(*) FROM weibo2 ) AS totel FROM weibo2  ORDER BY publish_time DESC LIMIT {},{}".format((page - 1) * pagesize, pagesize)

        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            resultlist = list(chain.from_iterable(results))
            return resultlist

        except Exception as e:

            raise e
        finally:
            self.db.close()  # 关闭连接


if __name__ == '__main__':
    pass


