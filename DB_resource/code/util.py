# -*- coding: utf-8 -*-

"""
Description: 数据处理工具类
Author:by 王林清 on 2021/11/1 15:36
FileName:util.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
import json
import os
from datetime import datetime

import opencc

cc = opencc.OpenCC('t2s')


def t2s_str(content: str):
    """
    :param content: 繁体字符串
    :return: 简体字符串
    """
    return cc.convert(content)


def t2s_list(content: list):
    """
    :param content: 字符串列表
    :return: 简体字符串列表
    """
    simplified_strings = []
    for string in content:
        simplified_strings.append(t2s_str(string))
    return simplified_strings


def get_file_path(dir_name):
    """
    :param dir_name: 目录
    :return: 目录下文件列表
    """
    filenames = os.listdir(dir_name)
    paths = []
    for filename in filenames:
        path = os.path.join(dir_name, filename)
        paths.append(path)
    return paths


def get_time_str():
    """
    :return: 当前时间的字符串值
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def save_json(filename: str, jsons, dir_name):
    """
    :param filename: 文件名
    :param jsons: 要存储的json对象(字典列表)
    :param dir_name: 存储目录
    """
    with open(f'{dir_name}/{filename}', 'w', encoding='utf-8') as f:
        json.dump(jsons, f, indent=4, ensure_ascii=False, skipkeys=True)


def save_split_json(filename: str, jsons, dir_name=r'./../database_json'):
    """
    分片存储json文件，每个最多10000首
    :param filename: 文件名
    :param jsons: 要存储的json对象(字典列表)
    :param dir_name: 存储目录
    """
    idx = 0
    while len(jsons) >= 1000:
        split_json = jsons[:1000]
        jsons = jsons[1000:]
        save_json(f'{filename}_{idx * 1000}.json', split_json, dir_name)
        idx += 1
    if idx:
        save_json(f'{filename}_{idx * 1000}.json', jsons, dir_name)
    else:
        save_json(f'{filename}.json', jsons, dir_name)


def get_json(path: str):
    """
    :param path: json文件路径
    :return: python字典列表
    """
    with open(path, 'r', encoding='utf-8') as f:
        jsons = json.load(f, encoding='utf-8')
    return jsons
