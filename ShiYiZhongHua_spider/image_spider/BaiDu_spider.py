import requests
import re
import os
import time
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
with open('author_2000.json','r',encoding='utf-8') as f:
    names = json.load(f)
    num = 0
    for name0 in names:
        name = name0["name"]
        # for name in name00:
        for i in range(1):
            name_1 = 'D:\\author_2000\\'
            url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+name+'画像'+'&pn='+str(i*30)
            res = requests.get(url,headers=headers)
            htlm_1 = res.content.decode()
            a = re.findall('"objURL":"(.*?)",',htlm_1)
            try:
                b=a[1]
                img = requests.get(b)
            except Exception as e:
                continue

            if not os.path.exists(name_1):
                os.makedirs(name_1)
            time = name0["time"]
            try:
                f = open(name_1+name+'_'+time+'.jpg','ab')
                print('---------正在下载图片----------')
                f.write(img.content)
                f.close()
            except Exception as e:
                continue
print('下载完成')
