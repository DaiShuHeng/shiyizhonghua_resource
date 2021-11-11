# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/1 14:30
FileName:poet.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from util import *

if __name__ == '__main__':
    dir_name = r'./../data/json'
    authors = {}
    poet_jsons = []

    paths = get_file_path(dir_name)
    author_song = paths.pop(0)
    author_tang = paths.pop(0)

    author_song_dicts = get_json(author_song)
    for author in author_song_dicts:
        name = t2s_str(author['name'])
        authors[name] = {
            'name': t2s_str(author['name']),
            'time': '宋',
            'desc': t2s_str(author['desc']),
        }

    author_tang_dicts = get_json(author_tang)
    for author in author_tang_dicts:
        name = t2s_str(author['name'])
        authors[name] = {
            'name': name,
            'time': '唐',
            'desc': t2s_str(author['desc']),
        }

    for path in paths:
        try:
            poet_json = get_json(path)
            for poet in poet_json:
                author = t2s_str(poet['author'])
                time = get_time_str()
                poet_jsons.append(
                    {
                        'title': t2s_str(poet['title']),
                        'author': authors[author],
                        'type': '诗',
                        'content': t2s_list(poet['paragraphs']),
                        'create_time': time,
                        'update_time': time,
                        'valid_delete': True
                    }
                )
        except Exception as ex:
            print(f'{path}:{ex}')

    save_split_json('poet', poet_jsons)
