# coding: utf-8
import os
import time
import requests
import webbrowser
from urllib import parse

url = 'https://weibo.com/ajax/statuses/hot_band'
hot_url_list = [None] * 55  # 内存优化
hot_color = {
    '爆': '\033[1;37;41m',
    '沸': '\033[1;31m',
    '热': '\033[1;33m',
    '新': '\033[0;32m',
    '无': '\033[37m',
}


def rush_hot():
    """ 刷新热搜列表 """
    os.system('clear')
    print(time.strftime('%Y年%m月%d日%H:%M:%S', time.localtime()), '实时微博热搜榜Top50')

    global hot_url_list
    hot_num = 0
    html_text = requests.get(url=url).json()
    band_list = html_text.get('data').get('band_list')

    for band in band_list:
        title = band.get('note')
        topic_flag = '%23' if band.get('topic_flag') else ''
        title_url = f'https://s.weibo.com/weibo?q={topic_flag}{parse.quote(title)}{topic_flag}'
        label_name = band.get('label_name')

        # 过滤广告
        if band.get('ad_channel'):
            continue

        # 构建全局热搜链接列表
        hot_url_list[hot_num] = title_url

        hot_num += 1
        print(f"{hot_color.get(label_name, '')}{hot_num}.{title}\033[0m", end='\n' if hot_num == 50 else '｜')


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
                webbrowser.open(hot_url_list[int(cmd) - 1])
            except AttributeError:
                pass
            except ValueError:
                pass
            except IndexError:
                pass
