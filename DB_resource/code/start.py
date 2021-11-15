# -*- coding: utf-8 -*-

"""
启动脚本

Author:by 王林清 on 2021/11/15 14:50
FileName:start.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""

import os
import re
import time

from util import get_file_path

start = time.time()
paths = get_file_path('.')
pattern = r'.*test.py|.*insert.*|.*util.py|.*__\w*__'
command = 'python {path}'

for path in paths:
    if not re.fullmatch(pattern, path, re.IGNORECASE):
        os.system(command.format(path=paths))
        print(f'{path} 已执行成功！')
os.system(command.format(path=r'./insertMongodb.py'))
print(f'共用时{time.time()-start}s, 数据插入完毕!')
