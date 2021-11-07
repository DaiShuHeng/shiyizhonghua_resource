# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/10/31 18:44
FileName:lunyu.py in chinese-poetry
Tools:PyCharm python3.8.4
"""
from util import get_time_str, save_split_json, get_json

if __name__ == '__main__':
    author = {
        'name': '孔子',
        'time': '春秋',
        'desc': '孔子（公元前551年9月28日～公元前479年4月11'
                '日），子姓，孔氏，名丘，字仲尼，鲁国陬邑（今山东省曲阜市）'
                '人，祖籍宋国栗邑（今河南省夏邑县），中国古代伟大的思想家、'
                '政治家、教育家，儒家学派创始人、“大成至圣先师”。 '
    }
    datas = []

    data = get_json(r'./../data/lunyu/lunyu.json')
    for dic in data:
        time = get_time_str()
        datas.append({
            'title': f"论语·{dic.pop('chapter')}",
            'author': author,
            'type': '古文',
            'content': dic.pop('paragraphs'),
            'create_time': time,
            'update_time': time,
            'valid_delete': True
        })

    save_split_json('lunyu', datas)
