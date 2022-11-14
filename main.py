from selenium import webdriver
from selenium.webdriver.common.by import By
import os
class script:
    '''欲查詢文字'''
    text = "" 
    options = None
    driver = None
    outputString = ""
    title = ""
    date = ""
    link = ""
    '''網址'''
    def get_link(self):
        link = self.driver.current_url
        print(link)
        return link    

    '''標題'''
    def get_title(self):
        titleText = self.driver.find_element(By.XPATH, "//div[@id='main-content']/div[3]/span[2]").text
        print(titleText)
        return titleText
    '''時間'''
    def get_time(self):
        timeText = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[4]/span[2]').text
        print(timeText)
        return(timeText)
    '''內文'''
    def get_article_text(self):
        articleText = self.driver.find_element(By.ID, "main-content").text
        partialText = articleText.split("\n")
        for i in range (4):
            articleText = articleText.replace(partialText[i]+"\n","")
            articleText = articleText.partition("--")[0]
        print(articleText)
        return articleText


    '''留言'''
    def get_comment(self):
        commentTexts = ""
        comments = self.driver.find_elements(By.CLASS_NAME, "push-content")
        # ipDateTime = driver.find_elements(By.CLASS_NAME, "push-ipdatetime")
        for i in range (len(comments)):
            commentTexts += comments[i].text.replace(": ", "")
            # if ipDateTime[i].text == ipDateTime[i-1].text:
            #     commentTexts[len(commentTexts)-1] += comments[i].text.replace(": ", "")
            # else:
            #     commentTexts.append(comments[i].text.replace(": ", ""))
        print(commentTexts)   
        return commentTexts

    def __init__(self,keyword):
    
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=self.options)
        self.driver.get("https://www.ptt.cc/bbs/index.html")
        self.text = keyword
        btn = self.driver.find_element(By.CLASS_NAME, "board")
        btn.click()

        btn2 = self.driver.find_element(By.CLASS_NAME, "btn-big")
        btn2.click()

        '''查詢'''
        textField = self.driver.find_element(By.NAME, "q")
        textField.clear()
        textField.send_keys(self.text)
        textField.send_keys(u'\ue007')

        '''熱門'''
        articleLabel = [] #最後整合起來的list
        articleLabel1 = [] #存推-噓不等於數字
        articleLabel2 = [] #存推-噓等於數字
        cnt = 0
        while cnt<19:
            nextPage = self.driver.find_element(By.XPATH, "//div[@class='action-bar']/div[2]/a[2]")
            GP = self.driver.find_elements(By.CLASS_NAME, "nrec")
            links = self.driver.find_elements(By.XPATH, "//div[@class = 'title']/a")
            for i in range(len(GP)):
                if GP[i].text == "爆" or GP[i].text.find("X") == 0 or GP[i].text == "":
                    articleLabel1.append([GP[i].text,  links[i].get_attribute("href")])
                else:
                    articleLabel2.append([int(GP[i].text),  links[i].get_attribute("href")])
            if nextPage.get_attribute("class") != "btn wide disabled": #沒有下一頁
                nextPage.click()
                cnt +=1
            else:
                break

        articleLabel1.sort(key = lambda a:ascii(a[0]), reverse  = True)
        articleLabel2.sort(key = lambda a:a[0], reverse  = True)
        for i in range(len(articleLabel1)):
            articleLabel.append(articleLabel1[i])
        for i in range(len(articleLabel2)):
            articleLabel2[i][0] =  str(articleLabel2[i][0])
            articleLabel.append(articleLabel2[i])
        # print(articleLabel)

        indexNum = 0
        i = 0
        # while i < 5:
        # ↓推-噓沒有X也不是空白的文章才抓
        if articleLabel[indexNum][0].find("X") == -1 and articleLabel[indexNum][0] != "": 
            self.driver.get(articleLabel[indexNum][1])
            self.link = self.get_link()
            self.title = self.get_title()
            self.date = self.get_time()
            articleText = self.get_article_text()
            comment = self.get_comment()
            self.outputString += articleText
            for j in range(len(comment)):
                self.outputString += comment[j]
            # print(outputString)
            indexNum += 1 #狗幹python for
            i += 1 #狗幹python for
        else:
            indexNum += 1 #狗幹python for
        self.driver.close() #這是關瀏覽器

        # #標題 網址 內文 留言