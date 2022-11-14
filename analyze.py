import jieba
import jieba.analyse
from main import script
from wordcloud import WordCloud
import os

class funshii:
    text = ""
    keywords = []
    link = ""
    title = ""
    date = ""
    def __init__(self,keyword):
        data = script(keyword)
        self.text =data.outputString
        self.link = data.link
        self.title = data.title
        self.date = data.date
        tags = []
        tag_count = []
        jieba.add_word('便當')
        jieba.analyse.set_stop_words(os.getcwd()+"/stop.txt")
        tags = jieba.analyse.extract_tags(self.text, topK=10) 
        print(tags)
        wordcloud = WordCloud(  font_path="msjh.ttf",  
                        scale=2, # zoom in
                        max_font_size = 200,  
                        #max_words=20, # 最多幾個字
                        background_color = '#FFFFFF', 
                        colormap = 'gray',
                        width=250, 
                        height=250
                        )
        
        wordcloud.generate_from_text(' '.join(tags))
        print(' '.join(tags))
        wordcloud.to_file(os.getcwd()+'/picture/'+keyword+'.png')
        self.keywords = []
        for i in range(len(tags)):
            
            d = {}
            d["keyword"] = tags[i]
            d["count"] = self.text.count(tags[i])
            self.keywords.append(d)
            # print(text.count(tags[i]))
            # tag_count.sort()
        print(self.keywords)
        


    