# coding: utf-8
import os
import sys
import time
import requests
import webbrowser
from lxml import etree

url = 'https://s.weibo.com/top/summary'
params = {
    'cate': 'realtimehot',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
}

hot_color = {
    '爆': '\033[1;37;41m',
    '沸': '\033[1;31m',
    '热': '\033[1;33m',
    '新': '\033[0;32m',
    '无': '\033[37m',
}
hot_dict = {}


def rush_hot():
    os.system('clear')
    print(time.strftime('%Y年%m月%d日%H:%M:%S', time.localtime()), '实时微博热搜榜Top50')
    hot_num = 0
    html_text = requests.get(url=url, params=params, headers=headers).text
    hot_list = etree.HTML(html_text).xpath('//div[@id="pl_top_realtimehot"]/table/tbody/tr')

    for hot in hot_list[1:]:
        hot_kind = hot.xpath('./td[@class="td-03"]/i/text()')[0] if hot.xpath('./td[@class="td-03"]/i/text()') else '无'
        hot_title = hot.xpath('./td[@class="td-02"]/a/text()')[0]
        # 过滤广告
        if hot_kind == '商':
            continue
        # 跳过推广
        if not hot.xpath('./td[@class="td-01 ranktop"]/text()')[0].isdigit():
            continue
        hot_num += 1
        hot_url = 'https://s.weibo.com' + hot.xpath('./td[@class="td-02"]/a/@href')[0]
        hot_dict[str(hot_num)] = hot_url
        print(f"{hot_color.get(hot_kind)}{hot_num}.{hot_title}\033[0m", end='\n' if hot == hot_list[-1] else '｜')


if __name__ == '__main__':
    rush_hot()

    while True:
        cmd = input('\033[36m选择编号（"r"刷新，"q"退出）: \033[0m')
        if cmd.upper() == 'R':
            rush_hot()
        elif cmd.upper() == 'Q':
            break
        else:
            try:
                webbrowser.open(hot_dict.get(cmd))
            except AttributeError:
                pass
