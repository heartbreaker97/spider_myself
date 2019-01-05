from wordcloud import WordCloud, ImageColorGenerator
import jieba
import matplotlib.pyplot as plt
from matplotlib import font_manager

import PIL.Image as image

class DataAnalysis:
    #读取文件
    def readtxt(self, filetxt):
        data = ''
        with open(filetxt, 'r',encoding='UTF-8') as f:
            for line in f:
                line = line.strip('\n')
                data += line
        return data

    #用jieba分词对输入文档进行分词，并保存至本地
    def segment(self,data):
        seg_list = " ".join(jieba.cut(data, cut_all=False))  # seg_list为str类型
        document_after_segment = open('word_spilt.txt', 'w+',encoding='UTF-8')
        document_after_segment.write(seg_list)
        document_after_segment.close()
        return seg_list

    #将停用词去除：
    def remove_stopword(self, seg_list):
        #初始化停用词去除后
        wordlist_stopword_remove = []
        #读取停用词生成list类型
        file_stop = open('stopwords1893.txt', 'r', encoding='UTF-8')
        stopwords = file_stop.read()
        file_stop.close()
        stopwords_list = stopwords.split('\n')

        #读取分词结果后生成list类型
        file_cut = open('word_spilt.txt', 'r', encoding='UTF-8')
        data_cut = file_cut.read()
        file_cut.close()
        data_cut_list = data_cut.split(' ')

        #去除data中的停用词，方案：如果datacut不在停用词那么获取
        for data in data_cut_list:
            if data not in stopwords_list:
                wordlist_stopword_remove.append(data)
        #写入本地并返回去除停用词的string类型
        file_cut_without_stopwords = open('word_spilt(without_stopwords).txt', 'w', encoding='UTF-8')
        without_stopwords = ' '.join(wordlist_stopword_remove)
        file_cut_without_stopwords.write(without_stopwords)
        file_cut_without_stopwords.close()
        return without_stopwords

    #生成词
    def into_wordcloud(self, without_stopwords):
        color_mask = plt.imread("mask.png")
        wc = WordCloud(
            #width: 800,

            # 设置字体，不指定就会出现乱码，注意字体路径
            font_path="GB2312.ttf",
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=2000,
            # 最大号字体
            max_font_size=70,
        )
        wc.generate(without_stopwords)
        image_colors = ImageColorGenerator(color_mask)
        wc.to_file("wordcloud.jpg")  # 保存图片
        #  显示词云图片
        plt.imshow(wc, interpolation="bilinear")
        plt.axis('off')

    #统计词频，以便生成柱状图
    def count_words(self, txtfile):
        word_count ={}
        file = open(txtfile, 'r', encoding='UTF-8')
        data = file.read()
        file.close()
        word_list = data.split(' ')
        #开始计数
        for word in word_list:
            if word not in word_count.keys():
                word_count[str(word)] = 1
            else:
                word_count[str(word)] += 1
        #del word_count['']
        #排序后变成list
        word_count_sort = sorted(word_count.items(), key=lambda x: x[1], reverse = True)
        #return word_count_sort
        return word_count_sort

    #统计人数，因为相比统计评论少了几步，统一写更麻烦，所以分开
    def count_name(self,txtfile):
        file = open(txtfile, 'r', encoding='UTF-8')
        name_data = file.read()
        file.close()
        name_data_list = name_data.split('\n')
        name_count = {}
        for word in name_data_list:
            if word not in name_count.keys():
                name_count[str(word)] = 1
            else:
                name_count[str(word)] += 1
        # 排序后变成list
        name_count_sort = sorted(name_count.items(), key=lambda x: x[1], reverse=True)
        return name_count_sort

    #生成柱状图
    def plot_data(self,lists, infor):
        import numpy as np
        fig, ax = plt.subplots()
        myfont = font_manager.FontProperties(fname='G:\python_shell\PycharmProjects\QzoneSpider_myself\spider\DataAnalysis\GB2312.ttf')
        name_list = []
        count_list = []
        for list in lists:
            name_list.append(list[0])
            count_list.append(list[1])
        N = 30
        y_pos = np.arange(N)

        colors = ['#FA8072']  # 这里是为了实现条状的渐变效果，以该色号为基本色实现渐变效果
        for i in range(len(name_list[:N]) - 1):
            colors.append('#FA' + str(int(colors[-1][3:]) - 1))

        rects = ax.barh(y_pos, count_list[:N], align='center', color=colors)

        ax.set_yticks(np.arange(N))
        ax.set_yticklabels(name_list[:N], fontproperties=myfont)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_title(infor, fontproperties=myfont, fontsize=17)
        ax.set_xlabel(u"出现次数", fontproperties=myfont)
        self.autolabel(rects, ax)
        plt.show()

    def autolabel(self,rects, ax):
        # fig, ax = plt.subplots()
        for rect in rects:
            width = rect.get_width()
            ax.text(1.03 * width, rect.get_y() + rect.get_height() / 2.,
                    '%d' % int(width), ha='center', va='center')

if __name__ == '__main__':
    analy = DataAnalysis()
    #生成词频的统计
    data = analy.readtxt('../comment_only.txt')
    seg_list = analy.segment(data)
    seg_list_remove_stopword = analy.remove_stopword(seg_list)
    analy.into_wordcloud(seg_list_remove_stopword)
    word_count_sort = analy.count_words('word_spilt(without_stopwords).txt')
    #print(word_count_sort)
    analy.plot_data(word_count_sort, '评论词频')

    #生成人数的统计
    name_count_sort = analy.count_name('../name_only.txt')
    analy.plot_data(name_count_sort,'评论人数')

