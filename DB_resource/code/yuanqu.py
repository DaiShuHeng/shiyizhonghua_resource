# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/2 16:40
FileName:yuanqu.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from util import *

if __name__ == '__main__':
    yq_jsons = []
    yq_json = get_json(r'./../data/yuanqu/yuanqu.json')
    for yq in yq_json:
        time = get_time_str()
        author = {
            'name': yq['author'],
            'time': '元',
            'desc': '',
        }
        yq_jsons.append(
            {
                'title': yq['title'],
                'author': author,
                'type': '曲',
                'content': yq['paragraphs'],
                'create_time': time,
                'update_time': time,
                'valid_delete': True,
            }
        )
    save_split_json('yuanqu', yq_jsons)
