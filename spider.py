import urllib
import requests
import json
import re
import time
#引入好写入数据库需要的DB类
import sys
sys.path.append('G:\python_shell\PycharmProjects\qzone_spider')
from DB import Db

class Qzone:

    #算出来gtk
    def get_gtk(self):
        p_skey = cookie['p_skey']
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
            g_tk = h & 2147483647
        return g_tk

    #得到uin
    def get_uin(self):
        uin = cookie['ptui_loginuin']
        return uin

    #发送http请求
    def send_http(self,url, data):

        url += urllib.parse.urlencode(data)
        try:
            res = requests.get(url, headers=header, cookies=cookie)
            print('读取成功')
        except Exception as e:
            print('读取错误：'+str(e))

        # 匹配出_preloadCallback之后的内容
        r = re.findall('\((.*)\)', res.text)[0]
        # 将json数据变成字典格式
        msg = json.loads(r)
        return msg

    #写入函数
    #count时用来写入txt文件的计数用的，写入数据库的时候可以不用
    #不写入数据库了，直接生成txt
    def write_to_db(self,m, file, count, file_name,uin=0, g_tk=0):
        if m['conlist'] is None:
            return 0
        if len(m['conlist'][0]) == 4:
            return 0
        # 查看是否有评论
        if ('commentlist' in m.keys()):
            for comment in m['commentlist']:
                #写入评论表
                #db.insert_topic_comment(comment['name'], comment['uin'], comment['content'], comment['createTime2'],m['tid'])
                file.write(comment['content'] + '\n')
                file_name.write(comment['name'] + '\n')
            #如果评论大于20条的话需要再进入新的界面，为了写入评论方便，所以在这里写
            #正常来说说说评论都不超过40条，所以这里写的最多的就是40条了，懒得改了
            if m['cmtnum'] > 20:
                data_more_20 = {
                    'uin': uin,
                    'topicId': uin+'_'+m['tid'],
                    'ftype': 0,
                    'sort': 0,
                    'order': 20,
                    'start': 20,
                    'num': 20,
                    't1_source': 'undefined',
                    'callback': '_preloadCallback',
                    'code_version': 1,
                    'format': 'jsonp',
                    'need_private_comment': 1,
                    'g_tk': g_tk,
                }
                url_more_20 = 'https://h5.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_getcmtreply_v6?'
                m_more_20 = self.send_http(url_more_20,data_more_20)
                #得到的m_more_20的字典结构 dict_keys(['code', 'data', 'message', 'result', 'right', 'smoothpolicy', 'subcode'])
                data = m_more_20['data']
                for comment in data['comments']:
                    file.write(comment['content'])
                    file_name.write(comment['poster']['name'] + '\n')


    #找到说说模块
    #pos是当前页面第一个说说的排序，一页20个
    def find_topic(self):
        #生成数据类
        #db = Db()
        #conti循环的标志，当为false时退出循环
        conti = True
        pos = 0
        count = 0
        g_tk = self.get_gtk()
        uin = self.get_uin()
        file = open('comment_only_test.txt','w',encoding='UTF-8')
        file_name = open('name_only_test.txt', 'w', encoding='UTF-8')
        while conti:
            #url必须在循环内，每次循环必须重置
            url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
            data = {
                'uin': uin,
                'pos': pos,
                'num': 20,
                'hostUin': uin,
                'replynum': 100,
                'callback': '_preloadCallback',
                'code_version': 1,
                'format': 'jsonp',
                'need_private_comment': 1,
                'g_tk': g_tk,
            }
            #下次翻页
            pos += 20

            msg = self.send_http(url,data,)

            # 这里爬说说结束
            if msg['msglist'] == None:
                file.close()
                print('无更多说说')
                return 0


            #得到的说说相关内容都在msglist(list类型)里面，msglist[i]是字典类型，可利用keys方法查看结构
            #说说内容conlist[0]['con'],另外转发的说说在conlist[1/2/3....]
            for m in msg['msglist']:
                #如果评论数大于10，则需要点进查看全部评论
                if m['cmtnum'] > 10:
                    data_more = {
                        'uin': uin,
                        'tid': m['tid'],
                        'ftype': 0,
                        'sort': 0,
                        'pos': 0,
                        'num': 20,
                        't1_source': 'undefined',
                        'callback': '_preloadCallback',
                        'code_version': 1,
                        'format': 'jsonp',
                        'need_private_comment': 1,
                        'g_tk': g_tk,
                    }
                    count += 1
                    url_more = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?'
                    m_more = self.send_http(url_more, data_more)
                    self.write_to_db(m_more, file, count, file_name, uin, g_tk)


                ##这里特殊，如果转发了说说并且没有配文字，而且原说说被删了，就会出现错误
                else:
                    if m['conlist'] is None:
                        continue
                    count += 1
                    self.write_to_db(m, file, count,file_name)

    #开始
    def start(self):
        self.find_topic()



if __name__ == '__main__':
    qzone = Qzone()
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Accepted-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    with open('cookie_dic.txt','r') as f:
        cookie = json.load(f)
    qzone.start()
