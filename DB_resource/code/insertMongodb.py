# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/2 21:32
FileName:insertMongodb.py in chinese-poetry
Tools:PyCharm python3.8.4
"""
from pymongo import MongoClient

from util import get_json

if __name__ == '__main__':
    ci_data = get_json(r'./../database_json/ci.json')
    client = MongoClient(host='47.98.214.74', port=27017)
    with client:
        db = client.project
        db.ci.insert_many(ci_data)
