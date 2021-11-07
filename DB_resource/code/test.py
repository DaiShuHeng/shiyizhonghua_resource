# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/10/31 16:22
FileName:test.py in chinese-poetry
Tools:PyCharm python3.8.4
"""
from datetime import datetime

from pymongo import collection
from util import *


def upsert_autotime(coll: collection.Collection, filterDict: dict,
                    updateDict: dict):
    """
    coll: MongoDB 集合
    filterDict: 过滤条件，须是主键
    updateDict: 更新字段内容
    """
    # 0 区
    dt0 = datetime.now()
    print(dt0)
    updateDict['update_time'] = dt0
    updateDict = {'$set': updateDict, '$setOnInsert': {'create_time': dt0}}

    return coll.update_one(filterDict, updateDict, upsert=True)


from pymongo import MongoClient

client = MongoClient(host='localhost', port=27017)

with client:
    # db = client.guwenTest
    # col = db['test']
    # # filter_dict = {'category': 'gg'}
    # # update_dict = {'category': 'hhby'}
    # # upsert_autotime(col, filter_dict, update_dict)
    # for x in col.find():
    #     print(x['create_time'].strftime('%Y-%m-%d'))
    #     print(x['update_time'].strftime('%Y-%m-%d'))
    # time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(time)
    paths = get_file_path(r'./../data/json')
    paths.pop()
    for path in paths:
        print(path)
