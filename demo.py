# -*-coding:utf-8-*-
import re
import requests
url = 'https://m.weibo.cn/detail/4758172798025786'

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
resp = requests.get(url=url, headers=headers)
html = resp.text
text = ''.join(re.findall('"text": (.*?",)', html))
print(text)


import datetime

d1 = datetime.date(2018, 3, 20)
d2 = datetime.date(2018, 1, 7)
print((d1 - d2).days)

a = '2015-04-07 04:30:03.628556'
d3 = datetime.datetime.strptime(str(a), "%Y-%m-%d %H:%M:%S.%f")
d4 = datetime.datetime.today()
d5 = (d4 - d3).days
print(d5, type(d5))
