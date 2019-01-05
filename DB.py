from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,MetaData
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, VARCHAR,BIGINT
from sqlalchemy.orm import sessionmaker, mapper

class Db:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:962464qwe@localhost:3306/spider?charset=utf8', echo=True, pool_size=200)

        #生成orm基类,是将表映射成对象的一个基类，所有表对象都要继承这个类
        self.base = MetaData()

        #生成说说表
        self.qzone_topic_test =Table(
            'qzone_topic_test',self.base,
             Column('id', String(25), primary_key=True),
             Column('content', VARCHAR(500)),
             Column('comment_count',Integer()),
             Column('create_time',DATETIME)
        )
        #生成评论表
        self.qzone_topic_comment_test = Table(
            'qzone_topic_comment_test',self.base,
            Column('id',Integer, primary_key=True, autoincrement= True),
            Column('name',String(20)),
            Column('qq_num',BIGINT),
            Column('content',String(1500)),
            Column('create_time',DATETIME),
            Column('tid',String(25),ForeignKey('qzone_topic_test.id'))
        )
        self.base.create_all(self.engine)
        #生成自定义的session类
        self.Session = sessionmaker()
        #将生成的数据库关联到session
        self.Session.configure(bind = self.engine)

    #插入评论表方法
    def insert_topic_comment(self, name, qq_num, content, create_time, tid):
        #生成session实例
        session = self.Session()
        #生成表的对象
        class Qzone_topic_comment_test(object):pass
        mapper(Qzone_topic_comment_test,self.qzone_topic_comment_test)
        Comment = Qzone_topic_comment_test()
        Comment.name = name
        Comment.qq_num = qq_num
        Comment.content =  content
        Comment.create_time = create_time
        Comment.tid = tid
        session.add(Comment)

        session.commit()
        session.query(Qzone_topic_comment_test).all()

    #插入说说表的方法
    def insert_topic(self, id, content, comment_count, create_time):
        #生成session实例
        session = self.Session()
        #生成表的对象
        class Qzone_topic_test(object):pass
        mapper(Qzone_topic_test,self.qzone_topic_test)
        Topic = Qzone_topic_test()
        Topic.id = id
        Topic.content =  content
        Topic.comment_count = comment_count
        Topic.create_time = create_time
        session.add(Topic)
        session.commit()
        session.query(Qzone_topic_test).all()

    #查询评论表
    '''def select_comment(self):
        # 生成session实例
        session = self.Session()
        class Comment(object):pass
        mapper(Comment,self.qzone_topic_comment_test)
        comment = Comment()
        self.Session().query(self.content).filter(comment.name=='泽强').all()
        #print(rows)

    def test(self):
        # 生成session实例
        session = self.Session()
        class Topic(object): pass
        mapper(Topic, self.qzone_topic)
        topic = Topic()
        print(topic.id)'''


if __name__ == '__main__':
    create_db = Db()
