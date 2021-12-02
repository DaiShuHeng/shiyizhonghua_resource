# 诗词爬虫
## 基于scrapy的诗词爬虫实现
### 项目介绍
#### 环境依赖
pip install scrapy 

#### 基本说明
完成对古诗文网诗词，作者，朝代的爬取
配置中禁用了robots，修改了USER_AGENT
爬取网站：https://www.gushiwen.cn/


#### 启动说明
1.命令行cmd 进入根目录ShiYiZhonHua_spider
2.运行scrapy crawl ShiYiZhonHua_spider
3.文件储存在gushi.csv中

#### 项目流程
- 创建一个scrapy爬虫项目 scrapy startproject ShiYiZhonHua 
- 进入项目spiders文件夹 输入scrapy genspider Spidername URL
- scrapy.cfg 项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）
- items.py 设置数据存储模板，用于结构化数据，如：Django的Model
- pipelines 数据处理行为，如：一般结构化的数据持久化
- settings.py 配置文件
- spiders 爬虫目录
- response中使用XPath、CSS查询十分普遍，因此，Scrapy提供了两个实用的快捷方式: response.xpath() 及 response.css():xpath() 及 .css() 方法返回一个类 SelectorList 的实例, 它是一个新选择器的列表。这个API可以用来快速的提取嵌套数据,需要调用 .extract() 方法

#### 注意事项
```text
1.在终端中进入存储项目的文件夹，然后使用“scrapy startproject 项目名”创建项目。

2.由终端进入 **最里层** spiders 文件夹内，使用“scrapy genspider 爬虫名字 <网页域名>” 来创建爬虫文件。其中，网页域名尽量不写 协议：http/https。

3.注：爬虫名不能与项目名相同。每爬取一个网站就创建一个爬虫项目。

4.运行爬虫文件：scrapy crawl 爬虫文件名

5.在 scrapy 中，一般的网站都会遵守 robots 协议。在 setting.py 中将 robots协议设置为 False，表示不用遵守。

6.注意 setting.py 中的 UA。
```

