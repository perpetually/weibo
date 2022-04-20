```
ps -ef |grep weibo |awk '{print $2}'|xargs kill -9
杀死所有微博开始的进程,减少内存占用

启动微博api
nohup  /usr/bin/python3   /spider/news/News_public_opinion/APi/api.py >/dev/null 2>&1 &

后台启动微博
nohup /opt/python36/bin/python3  /spider/United_front_news/weibos/weibo.py >/dev/null 2>&1 &
```
