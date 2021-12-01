# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/26 14:21
FileName:wjnbc.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from util import *

if __name__ == '__main__':
    wjnb_jsons = []
    wj_json = get_json(r'./../data/wjnb/weijin.json')
    nb_json = get_json(r'./../data/wjnb/nanbeichao.json')

    for wj in wj_json:
        time = get_time_str()
        author = {
            'name': wj['author'].split('·')[-1],
            'time': '魏晋',
            'desc': '',
        }
        content = [c.replace('\u3000', '') + '。' for c in
                   wj['content'].split('。')]
        content.pop()
        typ = '诗' if len(content[0]) == len(content[-1]) else '古文'
        wjnb_jsons.append(
            {
                'title': wj['title'],
                'author': author,
                'type': typ,
                'content': content,
                'create_time': time,
                'update_time': time,
                'valid_delete': True,
            }
        )

    for nb in nb_json:
        time = get_time_str()
        author = {
            'name': nb['author'],
            'time': '南北朝',
            'desc': '',
        }
        content = [c.replace('\u3000', '') + '。' for c in
                   nb['content'].split('。')]
        content.pop()
        typ = '诗' if len(content[0]) == len(content[-1]) else '古文'
        wjnb_jsons.append(
            {
                'title': nb['title'],
                'author': author,
                'type': typ,
                'content': content,
                'create_time': time,
                'update_time': time,
                'valid_delete': True,
            }
        )
    save_split_json('wjnb', wjnb_jsons)
