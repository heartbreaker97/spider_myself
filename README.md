# spider_myself
爬取自己qq空间说说评论人和评论内容

## 目录文件说明
    ├── DataAnalysis  分析文件
        ├── analysis.py  分析脚本
        ├── GB2312.ttf  字体文件
        ├── mask.png  词云生成图
        ├── stopwords1893.txt  停词文件
    ├── config.ini  配置文件
    ├── cookie_dic.py  生成cookie
    ├── DB.py  操作数据库类
    └── spider.py 爬虫类
    
## 代码运行流程
>1. 修改配置文件config.ini的配置，[qq]下的qq和pwd填写自己的qq和密码,[db]下暂时不需要，因为没有连接数据库
>2. 运行cookie.py，生成cookie文件
>3. 运行spider.py，爬取数据生成两个txt文件
>4. 运行DataAnalysis下的analysis.py，生成词频统计，词云，评论人统计的图

## 目前存在问题
>1. 用单线程爬数据，比较慢，有兴趣的话可以自己加上多线程
>2. 没用到数据库，直接用txt文件进行数据IO

## 注
> 如果生成的词频里面是有很多表情或者其他无意义的词，再停词文件中加上该词即可，例如出现[em]e400873[/em],那么在停词文件中再加一行内容为[em]e400873[/em],再运行以便analysis.py
