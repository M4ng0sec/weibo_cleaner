# coding=utf-8
import requests
import time
import json


# 在此复制微博网页版cookie, referer, url
web_cookie = ''
referer = ''
get_id_url = ''
# 根据自己微博数,设置要删除的最大页数, 一页大概十条微博
max_pages = 200

# 通过微博移动版获取微博id号,一次
def get_mid(session, page):
    url = get_id_url + str(page)
    response = session.get(get_id_url)
    json_data = json.loads(response.text)
    mids = []
    for i in json_data['cards'][1:]:
        mids.append(i['mblog']['id'])
        print mids
    return mids


# 通过id号删除微博
def del_by_id(session, mid):
    del_url = 'https://weibo.com/aj/mblog/del?ajwvr=6'
    form_data = {
        'mid': str(mid),
    }
    print session.post(del_url, data=form_data).text


# 发微博,测试用
def add_weibo(session, text):
    url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1510279745199'
    header = {
        'Cookie': web_cookie,
        'Referer': referer
    }
    session.headers.update(header)
    form_data = {
        'location': 'v6_content_home',
        'text': text,
        'appkey': '',
        'style_type': '1',
        'pic_id': '',
        'tid': '',
        'pdetail': '',
        'rank': '0',
        'rankid': '',
        'module': 'stissue',
        'pub_source': 'main_',
        'pub_type': 'dialog', ''
                              'isPri': '0',
        '_t': '0',
    }
    print session.post(url, data=form_data).text


if __name__ == '__main__':
    s = requests.session()
    header = {
        'Referer': referer,
        'Cookie': web_cookie
    }
    s.headers.update(header)

    # 获取微博id
    mids = []

    for i in range(1, max_pages):
        try:
            print i
            mids.extend(get_mid(s, i))
        except Exception, e:
            print e
            break

    # # 删除
    for i in range(len(mids)):
        del_by_id(s, mids[i])
        print str(i) + ' Done!!'
        # 设置删除间隔时间,如果被封IP了请自行去微博解锁,然后再运行脚本
        time.sleep(0.2)
