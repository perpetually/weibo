import datetime
import dbs
from flask import Flask, jsonify

app = Flask(__name__)

# 192.168.20.147

@app.route('/weibo/pagesize=<int:pagesize>/page=<int:page>', methods=['GET', 'POST'])
def index_month(pagesize, page):
    data_list = dbs.Tea().weibo(pagesize, page)
    n = 15
    payload = []
    for data in [data_list[i:i + n] for i in range(0, len(data_list), n)]:
        content = {"url": data[0], "content": data[1], "reposts_count": data[2],
                   "comments_count": data[3], "attitudes_count": data[4], "data_id": data[5],
                   "publish_time": str(data[6]),"forwardrt_content": data[7], "name": data[8],
                   "source": data[9], "images": eval(data[10]), "type": data[11], "level": data[12],
                   "gather_time": str(data[13]),
                   }
        payload.append(content)

    return jsonify({"internalErrorCode": 0, "msg": "success", "results": payload,
                    "pagination": {"current": page, "pageSize": pagesize, "startNumber": 1, "total": data[14],
                                   "totalPage": data[14] // pagesize}, "state": 200})


if __name__ == '__main__':
    app.debug = False
    app.run('0.0.0.0', 18003)
