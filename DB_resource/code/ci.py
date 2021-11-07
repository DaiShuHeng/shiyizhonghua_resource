# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/2 13:02
FileName:ci.py in chinese-ciry
Tools:PyCharm python3.8.4
"""
from util import get_time_str, get_json, get_file_path, save_json, \
    save_split_json

if __name__ == '__main__':
    dir_name = r'./../data/ci'

    authors = {}
    ci_jsons = []

    paths = get_file_path(dir_name)
    author_path = paths.pop(0)

    author_dicts = get_json(author_path)
    for author in author_dicts:
        name = author['name']
        authors[name] = {
            'name': name,
            'time': '宋',
            'desc': author['description'],
        }

    for path in paths:
        try:
            ci_json = get_json(path)
            for ci in ci_json:
                time = get_time_str()
                ci_jsons.append(
                    {
                        'title': ci['rhythmic'],
                        'author': authors[ci['author']],
                        'type': '词',
                        'content': ci['paragraphs'],
                        'create_time': time,
                        'update_time': time,
                        'valid_delete': True
                    }
                )
        except Exception as ex:
            print(f'{path}:{ex}')

    save_split_json('ci', ci_jsons)
