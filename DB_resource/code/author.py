# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/12/1 21:18
FileName:author.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""

from util import *

dir_path = r'./../database_json'
paths = get_file_path(dir_path)
authors = []
for path in paths:
    jsons = get_json(path)
    for data in jsons:
        author = {
            'name': data['author']['name'],
            'time': data['author']['time']
        }
        if author not in authors:
            authors.append(author)

save_split_json('author', authors, dir_name=r'./../../ShiYiZhonHua_spider/data')
