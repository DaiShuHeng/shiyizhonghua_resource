

# Elasticsearch使用手册

注：基于阿里云ESC服务器配置集群

## 一、安装

### 1、创建elastic用户

```bash
# 创建es用户，Elasticsearch不支持root用户运行 
# 创建用户
useradd es

# 为用户设置密码
passwd es
```

### 2、安装JDK

1. 执行以下命令，查看yum源中JDK版本。

```shell
yum list java*
```

2. 执行以下命令，使用yum安装JDK11。

```shell
yum -y install java-11-openjdk*
```

3. 执行以下命令，查看是否安装成功。

```shell
java -version
```

### 3、下载

1.官网下载安装包：https://www.elastic.co/cn/downloads/elasticsearch

2.使用ftp传输工具将压缩包传入/usr/local/目录下

3.解压安装包

```bash
# 解压安装包
tar -xvf elasticsearch.tar.gz
```

### 4、修改配置文件

1.修改配置文件elasticsearch.yml

```yml
#修改配置文件
vim conf/elasticsearch.yml
```

```yml
#设置ip地址，任意网络均可访问
network.host: 0.0.0.0 
#
## 集群名称
cluster.name: shiyizhonghua-es
## 节点名称
node.name: node01
## 设置该节点可以被选为master节点
node.master: true
## 设置该节点可以被选为数据节点
node.data: true
#
## 端口
http.port: 9200
transport.port: 9300
## 集群IP
discovery.zen.ping.unicast.hosts: ["114.55.236.49","116.62.195.199","47.47.100.193.135"]
cluster.initial_master_nodes: ["node01", "node02","node03"]
## 设置至少要两个节点同意才能为选为master
discovery.zen.minimum_master_nodes: 2
#
## 跨域相关设置
http.cors.enabled: true
http.cors.allow-origin: /.*/
#
## 暴露公网IP （如果是阿里云服务器，这里需要暴露公网IP，不然集群间会使用私有IP通信，导致通信问题。虚拟机不用配置）
network.publish_host: 114.55.236.49
```

2.修改配置文件jvm.options

```yml
# 说明:在Elasticsearch中如果，network.host不是localhost或者127.0.0.1的话，就会认为是生产环境， 会对环境的要求比较高，我们的测试环境不一定能够满足，一般情况下需要修改2处配置，如下: 
# 1:修改jvm启动参数
vim conf/jvm.options

# 根据自己机器情况修改
-Xms512m 
-Xmx512m
```

3.修改配置文件sysctl.conf

```yml
#2:一个进程在VMAs(虚拟内存区域)创建内存映射最大数量 
vim /etc/sysctl.conf

# 修改vm.max_map_count的值
vm.max_map_count=655360 

#配置生效
sysctl -p
```

4.修改/etc/security/limits.conf

```shell
vim /etc/security/limits.conf

添加如下内容:
* soft nofile 65536 
* hard nofile 131072 
* soft nproc 4096
* hard nproc 4096
```

5.启动elasticsearch

```shell
*# 切换到elsearch用户* 
su - elsearch 
cd bin 
# 启动 
./elasticsearch 或 ./elasticsearch -d #后台启动
```

6.验证是否成功启动

在浏览器中输入IP + 端口，如果返回如下信息则说明启动成功了。

默认端口号是9200

```bash
{
  "name" : "node01",
  "cluster_name" : "shiyizhonghua-es",
  "cluster_uuid" : "aag07AkTRreamm9BXWBD6w",
  "version" : {
    "number" : "7.15.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "93d5a7f6192e8a1a12e154a2b81bf6fa7309da0c",
    "build_date" : "2021-11-04T14:04:42.515624022Z",
    "build_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### 注：错误分析

#### 错误情况1

```bash
java.lang.RuntimeException: can not run elasticsearch as root
    atorg.elasticsearch.bootstrap.Bootstrap.initializeNatives(Bootstrap.java:111)
    at org.elasticsearch.bootstrap.Bootstrap.setup(Bootstrap.java:178)
    at org.elasticsearch.bootstrap.Bootstrap.init(Bootstrap.java:393)
    at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:170)
    at org.elasticsearch.bootstrap.Elasticsearch.execute(Elasticsearch.java:161)
    at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:86)
    at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:127)
    at org.elasticsearch.cli.Command.main(Command.java:90)
    at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:126)
    at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:92)
For complete error details, refer to the log at /soft/elsearch/logs/elasticsearch.log

ERROR CLogger.cc@310 Cannot log to named pipe /tmp/elasticsearch-5834501324803693929/controller_log_381 as it could not be opened for writing
2020-09-22 02:59:39,537263 UTC [536] INFO  Main.cc@103 Parent process died - ML controller exiting
```

说明你没有切换成 **elsearch** 用户，因为不能使用 **root** 用户去操作 *ElasticSearch*

```bash
su - es
```

#### 错误情况2

```bash
[1]:max file descriptors [4096] for elasticsearch process is too low, increase to at least[65536]
```

解决方法：切换到 **root** 用户，编辑 **limits.conf** 添加如下内容

```bash
vi /etc/security/limits.conf

# ElasticSearch添加如下内容:
* soft nofile 65536
* hard nofile 131072
* soft nproc 2048
* hard nproc 4096
```

#### 错误情况3

```bash
[2]: max number of threads [1024] for user [elsearch] is too low, increase to at least[4096]
```

也就是最大线程数设置的太低了，需要改成 **4096**

```bash
#解决：切换到root用户，进入limits.d目录下修改配置文件。
vi /etc/security/limits.d/90-nproc.conf
#修改如下内容：
* soft nproc 1024
#修改为
* soft nproc 4096
```

#### 错误情况4

```bash
[3]: system call filters failed to install; check the logs and fix your configuration or disable system call filters at your own risk
```

解决：**Centos6** 不支持 **SecComp**，而 **ES5.2.0** 默认 **bootstrap.system_call_filter** 为  true

```bash
vim config/elasticsearch.yml
# 添加
bootstrap.system_call_filter: false
bootstrap.memory_lock: false
```

#### 错误情况5

```java
Exception in thread "main" org.elasticsearch.bootstrap.BootstrapException: java.nio.file.AccessDeniedException: /soft/elsearch/config/elasticsearch.keystore
Likely root cause: java.nio.file.AccessDeniedException: /soft/elsearch/config/elasticsearch.keystore
  at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:90)
  at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
  at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:116)
  at java.base/sun.nio.fs.UnixFileSystemProvider.newByteChannel(UnixFileSystemProvider.java:219)
  at java.base/java.nio.file.Files.newByteChannel(Files.java:375)
  at java.base/java.nio.file.Files.newByteChannel(Files.java:426)
  at org.apache.lucene.store.SimpleFSDirectory.openInput(SimpleFSDirectory.java:79)
  at org.elasticsearch.common.settings.KeyStoreWrapper.load(KeyStoreWrapper.java:220)
  at org.elasticsearch.bootstrap.Bootstrap.loadSecureSettings(Bootstrap.java:240)
  at org.elasticsearch.bootstrap.Bootstrap.init(Bootstrap.java:349)
  at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:170)
  at org.elasticsearch.bootstrap.Elasticsearch.execute(Elasticsearch.java:161)
  at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:86)
  at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:127)
  at org.elasticsearch.cli.Command.main(Command.java:90)
  at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:126)
  at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:92)
```

也就是说该文件还是所属于**root** 用户，而我们使用 **elsearch** 用户无法操作，所以需要把它变成**elsearch** 

```
chown elsearch:elsearch elasticsearch.keystore
```

### 另：一些linux命令

#### 切换用户

```shell
su - XX
```

#### 添加sudoers

```shell
#添加sudoers文件的写权限
chmod u+w /etc/sudoers

vi /etc/sudoers

#找到 root ALL=(ALL) ALL 这一行,在他下面添加xxx ALL=(ALL) ALL (这里的xxx是你的用户名)

#撤销sudoers文件写权限
chmod u-w /etc/sudoers
```

#### 查看后台进程

```sh
ps -ef | grep elastic

#杀掉进程（xxx为端口号）
kill -9 xxx
```

## 二、ElasticSearchHead可视化工具

### 通过Chrome插件安装

打开 **Chrome** 的应用商店，即可安装 https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm

![eshead](./eshead.png)

## 三、kibana

部署在本地，通过更改配置文件即可连接服务器

### 1、安装

```sh
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.15.2-linux-x86_64.tar.gz
```

### 2、解压缩

```sh
tar -xzf kibana-7.15.2-linux-x86_64.tar.gz
```

### 3、配置文件

```sh
vim /config/kibana.yml

server.port: 5601
server.host: "localhost"
server.name: "localhost"
elasticsearch.hosts: ["http://114.55.236.49:9200","http://47.100.193.135:9200","http://116.62.195.199:9200"]
i18n.locale: "zh-CN"
```

### 4、启动

```sh
./bin/kibana

#后台运行
nohup /usr/local/kibana/bin/kibana &
```

## 四、Metricbeat

监测集群情况

### 1、安装（与Elasticsearch版本保持一致且安装在同一服务器内）

```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.15.2-linux-x86_64.tar.gz
tar xzvf metricbeat-7.15.2-linux-x86_64.tar.gz
```

### 2、在 Metricbeat 中启用并配置 Elasticsearch x-pack 模块

```sh
#启用模块
./metricbeat modules enable elasticsearch-xpack

#配置模块
cd modules.d
vim elasticsearch-xpack.yml

#将服务器地址添加到hosts设置
hosts: ["http://114.55.236.49:9200"]
```

### 3、配置 Metricbeat 以发送至监测集群

```sh
vim metricbeat.yml
```

```yml
output.elasticsearch:  
	hosts: ["114.55.236.49:9200","47.100.193.135:9200","116.62.195.199:9200"] 
```

### 4、启动Metricbeat

```sh
sudo chown root metricbeat.yml 
sudo chown root modules.d/system.yml 
sudo ./metricbeat -e

#后台运行
nohup ./metricbeat -e -c metricbeat.yml -d "publish" & > nohup.out
```

## 五、Monstache

数据库中间件：同步MongoDB与Elasticsearch数据

### 1、安装

下载地址：https://github.com/rwynn/monstache/releases

版本信息：

| Monstache version | Git branch (used to build plugin) | Docker tag   | Description             | Elasticsearch   | MongoDB      | Status     |
| ----------------- | --------------------------------- | ------------ | ----------------------- | --------------- | ------------ | ---------- |
| 6                 | rel6                              | rel6, latest | MongoDB, Inc. go driver | Version 7+      | Version 2.6+ | Supported  |
| 5                 | rel5                              | rel5         | MongoDB, Inc. go driver | Version 6       | Version 2.6+ | Supported  |
| 4                 | master                            | rel4         | mgo community go driver | Version 6       | Version 3    | Deprecated |
| 3                 | Rel3                              | rel3         | mgo community go driver | Version 2 and 5 | Version 3    | Deprecated |

解压缩下载并调整您的 PATH 变量

查看版本号

```sh
monstache -v
```

### 2、修改配置文件

```sh
vim config.toml
```

```toml
# connect to MongoDB using the following URL 这项配置添加Mongodb的地址
mongo-url = "mongodb://用户名:密码@服务器地址:27017"
# connect to the Elasticsearch REST API at the following node URLs
elasticsearch-urls = ["http://服务器地址:9200"]
direct-read-namespaces = ["shiyizhonghua.data"]  #指定mongo中要导出数据库和集合
#elasticsearch-user = ""
#elasticsearch-password = ""    #ES服务器的密码
elasticsearch-max-conns = 8
dropped-collections = true
dropped-databases = true
resume = true
resume-strategy = 0
verbose = true
elasticsearch-validate-pem-file = false
[[mapping]]
namespace = "shiyizhonghua.data"
index = "shiyizhonghua"      #映射到ES中的索引名称
```

### 3、运行

```sh
monstache -f /path/to/config.toml
```

## 六、插件（ik、pinyin）

### 1、安装

```shell
#注意插件的版本要与es的版本一致
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.15.2/elasticsearch-analysis-ik-7.15.2.zip

./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v7.15.2/elasticsearch-analysis-pinyin-7.15.2.zip
```

### 2、使用

新建索引

```
PUT /syzh
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ik_smart_pinyin": {
          "type": "custom", //自定义分析器
          "tokenizer": "ik_smart", //ik插件
          "filter": [
            "pinyin_filter" //筛选
          ]
        },
        "ik_max_word_pinyin": {
          "type": "custom",
          "tokenizer": "ik_max_word",
          "filter": [
            "pinyin_filter"
          ]
        }
      },
      "filter": {
        "pinyin_filter": {
          "type": "pinyin", //pinyin插件
          "keep_separate_first_letter": false,
          "keep_full_pinyin": true,
          "keep_original": true,
          "limit_first_letter_length": 16,
          "lowercase": true,
          "remove_duplicated_term": true
        }
      }
    },
    "number_of_shards": 3, //分片数量
    "number_of_replicas": 2 //副本数量
  }
}
```

配置mapping

```
PUT syzh/_mapping
{
  "properties": {
    "author": {
      "properties": {
        "desc": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "name": {
          "type": "text",
          "analyzer": "ik_max_word_pinyin",
          "search_analyzer": "ik_smart_pinyin",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "time": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    },
    "content": {
      "type": "text",
      "analyzer": "ik_max_word_pinyin",
      "search_analyzer": "ik_smart_pinyin",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "create_time": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "title": {
      "type": "text",
      "analyzer": "ik_max_word_pinyin",
      "search_analyzer": "ik_smart_pinyin",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "type": {
      "type": "text",
      "analyzer": "ik_max_word_pinyin",
      "search_analyzer": "ik_smart_pinyin",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "update_time": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "valid_delete": {
      "type": "boolean"
    }
  }
}
```

pinyin插件可选参数

```
keep_first_letter:启用此选项时，例如：刘德华> ldh，默认值：true
keep_separate_first_letter:启用此选项后，将单独保留首字母，例如：刘德华> l, d, h, 默认值：false，注意：由于术语过于频繁，查询结果可能过于模糊
limit_first_letter_length:设置 first_letter 结果的最大长度，默认值：16
keep_full_pinyin:启用此选项时，例如：刘德华> [ liu, de, hua]，默认值：true
keep_joined_full_pinyin:启用此选项时，例如：刘德华> [ liudehua]，默认值：false
keep_none_chinese:结果中保留非中文字母或数字，默认：true
keep_none_chinese_together:将非中文字母放在一起，默认值：true，例如：DJ音乐家-> DJ, yin, yue, jia, 当设置为 时false，例如：DJ音乐家-> D, J, yin, yue, jia, 注意：keep_none_chinese应先启用
keep_none_chinese_in_first_letter:首字母保留非中文字母，例如：刘德华AT2016-> ldhat2016，默认：true
keep_none_chinese_in_joined_full_pinyin:将非中文字母保留在连接全拼音中，例如：刘德华2016-> liudehua2016，默认值：false
none_chinese_pinyin_tokenize:如果非中文字母是拼音，则将它们拆分成单独的拼音词，默认：true，例如：liudehuaalibaba13zhuanghan-> liu, de, hua, a, li, ba, ba, 13, zhuang, han, , 注意： keep_none_chinese并且keep_none_chinese_together应该先启用
keep_original:启用此选项时，也会保留原始输入，默认值：false
lowercase:小写非中文字母，默认：true
trim_whitespace:默认值：真
remove_duplicated_term:启用此选项后，将删除重复的术语以保存索引，例如：de的> de，默认值：false，注意：可能会影响与位置相关的查询
ignore_pinyin_offset:6.0后，offset被严格限制，不允许重叠token，有了这个参数，overlapped token将被ignore offset允许，请注意，所有与位置相关的查询或高亮都会变得不正确，你应该使用多字段并为不同的设置指定不同的设置查询目的。如果您需要偏移，请将其设置为false。默认值：真。
```

### 3、一些报错解决

#### (1):权限问题

```java
WARNING: plugin requires additional permissions
```

解决办法：以root用户执行安装命令

```
su - root
```

#### (2):重复插件

```java
Exception in thread "main" java.lang.IllegalStateException: duplicate plugin: - Plugin information:
Name: analysis-pinyin
Description: Pinyin Analysis for Elasticsearch
Version: 7.15.2
Elasticsearch Version: 7.15.2
Java Version: 1.8
Native Controller: false
Licensed: false
Type: isolated
Extended Plugins: []
 * Classname: org.elasticsearch.plugin.analysis.pinyin.AnalysisPinyinPlugin
        at org.elasticsearch.plugins.PluginsService.findBundles(PluginsService.java:406)
        at org.elasticsearch.plugins.PluginsService.getPluginBundles(PluginsService.java:397)
        at org.elasticsearch.plugins.InstallPluginAction.jarHellCheck(InstallPluginAction.java:829)
        at org.elasticsearch.plugins.InstallPluginAction.loadPluginInfo(InstallPluginAction.java:804)
        at org.elasticsearch.plugins.InstallPluginAction.installPlugin(InstallPluginAction.java:850)
        at org.elasticsearch.plugins.InstallPluginAction.execute(InstallPluginAction.java:233)
        at org.elasticsearch.plugins.InstallPluginCommand.execute(InstallPluginCommand.java:84)
        at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:75)
        at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:114)
        at org.elasticsearch.cli.MultiCommand.execute(MultiCommand.java:95)
        at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:114)
        at org.elasticsearch.cli.Command.main(Command.java:79)
        at org.elasticsearch.plugins.PluginCli.main(PluginCli.java:36)
```

解决办法：删除已下载插件

```shell
# 查看插件列表
bin/elasticsearch-plugin list

cd plugins/
ls -a
rm -rf xxx
```

## 七、查询

基于JSON，查询DSL定义查询

### 1、查询所有文档

```http
GET shiyizhonghua/_search
{
  "query": {
    "match_all": {}
  }
}
```

"query":代表一个查询对象，里面可以有不同的查询属性

"match_all":查询类型 (match_all、match、term、range等)

{查询条件}:查询条件根据类型不同，写法也有差异

**查询结果：**

```http
{
  "took" 【查询花费时间，单位毫秒】: 35,
  "timed_out" 【是否超时】: false,
  "_shards" 【分片信息】: {
    "total"【总数】 : 3,
    "successful"【成功数】 : 3,
    "skipped"【忽略数】 : 0,
    "failed"【失败数】 : 0
  },
  "hits" 【搜索命中结果】: {
    "total"【搜索条件匹配的文档总数】 : {
      "value"【总命中计数的值】 : 10000,
      "relation"【计数规则，eq表示计数准确、gte表示计数不准确】 : "gte"
    },
    "max_score"【匹配度分值】 : 1.0,
    "hits"【命中结果集合】 : [···
    }
   ]
  }
}   
```

### 2、匹配查询

```http
GET shiyizhonghua/_search
{
  "query": {
    "match": {
      "author.name": "杜甫"
    }
  }
}
```

### 3、字段匹配查询

multi_match与match类似，它的特点是可以在多个字段中查询

```http
GET shiyizhonghua/_search
{
  "query": {
    "multi_match": {
      "query": "杜甫",
      "fields": ["author.name","content"]
    }
  }
}
```

### 4、关键词精确查询

term查询，精确的关键词匹配查询，不对查询条件进行分词

```http
GET shiyizhonghua/_search
{
  "query": {
    "term": {
      "author.name": {
        "value": "陶渊明"
      }
    }
  }
}
```

### 5、多关键词精确查询

terms查询和term查询一样，但允许指定多值进行匹配。

如果这个字段包含了指定值的任何一个值，那么这个文档满足条件

```http
GET shiyizhonghua/_search
{
  "query": {
    "terms": {
      "author.name": [
        "李白",
        "杜甫"
      ]
    }
  }
}
```

### 6、指定查询字段

默认情况下，Elasticsearch 在搜索的结果中，会把文档中保存在_source 的所有字段都返回。 如果我们只想获取其中的部分字段，我们可以添加_source 的过滤

```http
GET shiyizhonghua/_search
{
  "_source": ["author.name","author.time","type","content","author.desc","title"]
  , "query": {
    "terms": {
      "title": ["琵琶行"]
    }
  }
}
```

### 7、过滤字段

includes:指定想要显示的字段

excludes:指定不想要显示的字段

```http
GET shiyizhonghua/_search
{
  "_source": {
    "includes": ["author.name","author.time","type","content","author.desc","title"]
  }
  , "query": {
    "terms": {
      "title": ["琵琶行"]
    }
  }
}
```

### 8、组合查询

`bool`把各种其它查询通过`must`(必须 )、`must_not`(必须不)、`should`(应该)的方式进行组合

```http
GET shiyizhonghua/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "author.name": "李白"
          }
        }
      ]
      , "must_not": [
        {
          "match": {
            "author.time": "宋"
          }
        }
      ]
    }
  }
}
```

### 9、范围查询

range 查询找出那些落在指定区间内的数字或者时间。range 查询允许以下字符

| 操作符 | 说明       |
| ------ | ---------- |
| gt     | 大于>      |
| gte    | 大于等于>= |
| lt     | 小于<      |
| lte    | 小于等于<= |

```http
GET shiyizhonghua/_search
{
  "query": {
    "range": {
      "update_time": {
        "gte": 10,
        "lte": 20
      }
    }
  }
}
```

### 10、模糊查询

返回包含与搜索字词相似的字词的文档

fuzziness可修改编辑距离。一般为默认值AUTO，根据术语的长度生成编辑距离

```http
GET shiyizhonghua/_search
{
"query": {
   "fuzzy": {
     "author.time": {
       "value": "宋"，
       "fuzziness": "2"
      }
    }
  }
}
```

### 11、单字段排序

sort 可以让我们按照不同的字段进行排序，并且通过 order 指定排序的方式 （desc 降序，asc 升序）

```http
GET shiyizhonghua/_search
{
  "query": {
    "term": {
      "author.name": {
        "value": "李白"
      }
    }
  },
  "sort": [
    {
      "author.name.keyword": {
        "order": "desc"
      }
    }
  ]
}
```

### 12、多字段排序

假定我们想要结合使用 author.name.keyword 和 _score 进行查询，并且匹配的结果首先按照姓名排序，然后按照相关性得分排序

```http
GET shiyizhonghua/_search
{
  "query": {
    "term": {
      "author.name": {
        "value": "李白"
      }
    }
  },
  "sort": [
    {
      "author.name.keyword": {
        "order": "desc"
      }
    },
    {
      "_score": {
        "order": "desc"
      }
    }
  ]
}
```

### 13、高亮查询

在进行关键字搜索时，搜索出的内容中的关键字会显示不同的颜色，称之为高亮

Elasticsearch 可以对查询内容中的关键字部分，进行标签和样式(高亮)的设置。 在使用 match 查询的同时，加上一个 highlight 属性:

- pre_tags:前置标签
- post_tags:后置标签
- fields:需要高亮的字段
- title:这里声明 title 字段需要高亮，后面可以为这个字段设置特有配置，也可以空

```
GET shiyizhonghua/_search
{
  "query": {
    "term": {
      "author.name": {
        "value": "李白"
      }
    }
  },
  "highlight": {
    "pre_tags": "<font color='red'>",
    "post_tags": "</font>",
    "fields": {
      "author.name": {}
    }
  }
}
```

### 14、分页查询

from:当前页的起始索引，默认从 0 开始。 from = (pageNum - 1) * size 

size:每页显示多少条

```http
GET shiyizhonghua/_search
{
  "query": {
    "term": {
      "author.name": {
        "value": "李白"
      }
    }
  },
  "from": 0,
  "size": 10
}
```

### 15、聚合查询

聚合允许使用者对 es 文档进行统计分析，类似与关系型数据库中的 group by，当然还有很 多其他的聚合，例如取最大值、平均值等等

#### 对某个字段取最大值 max

```http
{
 "aggs":{
	"max_age":{
		"max":{"field":"age"}
		} 
	},
	"size":0 
}
```

#### 对某个字段取最小值 min

```http
{
 "aggs":{
	"min_age":{
		"min":{"field":"age"}
		} 
	},
	"size":0 
}
```

#### 对某个字段求和 sum

```http
{
 "aggs":{
	"sum_age":{
		"sum":{"field":"age"}
		} 
	},
	"size":0 
}
```

#### 对某个字段取平均值 avg

```http
{
 "aggs":{
	"avg_age":{
		"avg":{"field":"age"}
		} 
	},
	"size":0 
}
```

#### 对某个字段的值进行去重之后再取总数

```http
{
 "aggs":{
	"distinct_age":{
		"cardinality":{"field":"age"}
		} 
	},
	"size":0 
}
```

#### State 聚合

对某个字段一次性返回 count，max，min，avg 和 sum 五个指标

```http
{
 "aggs":{
	"stats_age":{
		"stats":{"field":"age"}
		} 
	},
	"size":0 
}
```

### 16、桶聚合查询

桶聚和相当于 sql 中的 group by 语句

#### terms 聚合，分组统计

```http
{
  "aggs": {
    "age_groupby": {
      "terms": {
        "field": "age"
      }
    }
  },
  "size": 0
}
```

#### 在 terms 分组下再进行聚合

```http
{
  "aggs": {
    "age_groupby": {
      "terms": {
        "field": "age"
      },
      "aggs":
      {
      	"sum":{"field":"age"}
      }
    }
  },
  "size": 0
}
```

