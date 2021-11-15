# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/15 16:09
FileName:sishuwujing.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from util import *


if __name__ == '__main__':
    dir_name = r'./../data/sishuwujing'

    dx_author = {
        'name': '曾子',
        'time': '春秋',
        'desc': '曾子（前505年－前435年），姒姓，曾氏，名参（学术界有两种说法，一读shēn，'
                '一读cān），字子舆，鲁国南武城（今山东平邑，一说山东嘉祥）人。春秋末年思想'
                '家，儒家大家，孔子晚年弟子之一，儒家学派的重要代表人物，夏禹后代。其父曾'
                '点，字皙，七十二贤之一，与子曾申同师孔子。倡导以“孝恕忠信”为核心的儒家思想'
                '，“修齐治平”的政治观，“内省慎独”的修养观，“以孝为本”的孝道观至今仍具有极其'
                '宝贵的社会意义和实用价值。曾子参与编制了《论语》、撰写《大学》、《孝经》、'
                '《曾子十篇》等作品。'
    }
    mz_author = {
        'name': '孟子',
        'time': '战国',
        'desc': '孟子，名轲，字子舆（约公元前372年—公元前289年），邹国（今山东邹城东南）人。'
                '战国时期哲学家、思想家、政治家、教育家，是孔子之后、荀子之前的儒家学派的代表'
                '人物，与孔子并称“孔孟”。孟子宣扬“仁政”，最早提出“民贵君轻”思想，被韩愈列为'
                '先秦儒家继承孔子“道统”的人物，元朝追封为“亚圣”。孟子的言论著作收录于'
                '《孟子》一书。其中《鱼我所欲也》、《得道多助，失道寡助》、《寡人之于国也》、'
                '《生于忧患，死于安乐》和《富贵不能淫》等篇编入中学语文教科书中。'
    }
    zy_author = {
        'name': '子思',
        'time': '春秋',
        'desc': '孔伋（前483年－前402年），字子思，鲁国人，孔子的嫡孙、孔子之子孔鲤的儿子。'
                '大约生于周敬王三十七年（公元前483年），卒于周威烈王二十四年（公元前402年）'
                '，享年82岁。春秋时期著名的思想家。受教于孔子的高足曾参，孔子的思想学说由曾'
                '参传子思，子思的门人再传孟子。后人把子思、孟子并称为思孟学派，因而子思上承'
                '曾参，下启孟子，在孔孟“道统”的传承中有重要地位。《史记·孟子荀卿列传》称孟子'
                '求学于子思的门人，《孟子题辞》则称孟子是子思的学生。子思在儒家学派的发展史上'
                '占有重要的地位，他上承孔子中庸之学，下开孟子心性之论，并由此对宋代理学产生了'
                '重要而积极的影响。因此，北宋徽宗年间，子思被追封为“沂水侯”；元文宗至顺元年'
                '（公元1330年），又被追封为“述圣公”，后人由此而尊他为“述圣”，受儒教祭祀。'
    }

    datas = []

    paths = get_file_path(dir_name)
    dx_path = paths.pop(0)
    mz_path = paths.pop(0)
    zy_path = paths.pop(0)

    dx_json = get_json(dx_path)
    mz_jsons = get_json(mz_path)
    zy_json = get_json(zy_path)

    time = get_time_str()

    datas.append({
        'title': '大学',
        'author': dx_author,
        'type': '古文',
        'content': t2s_list(dx_json['paragraphs']),
        'create_time': time,
        'update_time': time,
        'valid_delete': True
    })

    for mz_json in mz_jsons:
        datas.append({
            'title': f"孟子·{t2s_str(mz_json['chapter'])}",
            'author': mz_author,
            'type': '古文',
            'content': t2s_list(mz_json['paragraphs']),
            'create_time': time,
            'update_time': time,
            'valid_delete': True
        })

    datas.append({
        'title': '中庸',
        'author': zy_author,
        'type': '古文',
        'content': t2s_list(zy_json['paragraphs']),
        'create_time': time,
        'update_time': time,
        'valid_delete': True
    })

    save_split_json('sishuwujing', datas)
