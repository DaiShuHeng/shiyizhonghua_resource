# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/15 15:45
FileName:caocao.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from util import *

if __name__ == '__main__':
    author = {
        'name': '曹操',
        'time': '汉',
        'desc': '魏武帝曹操（155年—220年3月15日），字孟德，一名吉利，小字阿瞒。沛国谯县'
                '（今安徽省亳州市）人。中国古代杰出的政治家、军事家、文学家、书法家、诗人。'
                '东汉末年权相，太尉曹嵩之子，曹魏的奠基者。曹操少年机警，任侠放荡，不治行业。'
                '二十岁时，举孝廉为郎，授洛阳北部尉。后任骑都尉，参与镇压黄巾军。迁济南相，'
                '奏免贪吏，禁断淫祀。征为东郡太守，不就，称疾归家。及董卓擅政，乃散家财起兵，'
                '与袁绍等共讨董卓。初平三年（192年）据兖州，分化诱降黄巾军三十余万，选其精锐'
                '编为青州军，自此兵力大振，先后击败袁术、陶谦、吕布等部。建安元年（196年）'
                '，迎汉献帝至许（今河南许昌东），自为司空，行车骑将军事，总揽朝政。建安五年'
                '（200年），在官渡之战中大败袁绍主力，又先后削平袁尚、袁谭等势力。建安十二年'
                '（207年），击破乌桓，统一北方。建安十三年（208年），进位丞相。同年进攻荆州'
                '，与孙权、刘备联军展开赤壁之战，败归。建安十八年（213年），封魏公。建安二'
                '十年（215年），征张鲁，取汉中。次年进爵为魏王。建安二十五年（220年），病死'
                '于洛阳，儿子曹丕代汉称帝后，追尊曹操为太祖武皇帝，葬于高陵。'
    }

    datas = []

    data = get_json(r'./../data/caocaoshiji/caocao.json')
    for dic in data:
        time = get_time_str()
        datas.append({
            'title': dic['title'],
            'author': author,
            'type': '诗',
            'content': dic['paragraphs'],
            'create_time': time,
            'update_time': time,
            'valid_delete': True
        })

    save_split_json('caocao', datas)
