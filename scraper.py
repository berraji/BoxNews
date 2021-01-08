import requests
from bs4 import BeautifulSoup
import time
from db import *
import json
import os


class ArticleScraper:
    def __init__(self,url):
        self.url = url
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html,"html.parser")
        self.title = self.get_title()
        self.category = self.get_category()
        self.id = self.get_id()
        #image principale
        self.img_url = self.get_img()
        self.date = self.get_date()
        self.author = self.get_author()
        self.tag_list = self.toS(self.get_tagList())
        self.body = self.get_body()
    def get_html(self):
        response = requests.get(self.url)
        html = response.content
        return html
    def get_id(self):
        return os.path.basename(self.url)
    def get_title(self):
        title_tag = self.soup.select(".story-body__h1")
        if(title_tag.__len__() == 0):
            title_tag = self.soup.select(".vxp-media__headline")
        
        if(title_tag.__len__()):
            return title_tag[0].get_text()
        return ""
    def get_img(self):
        img_tag = self.soup.findAll('img',attrs = {'class':'js-image-replace'})
        if(img_tag.__len__() == 0):
            img_tag = self.soup.findAll('img',attrs = {'class':'lead-video-placeholder'})
        if(img_tag.__len__()):
            return img_tag[0]['src']
        return ""

    def get_date(self):
        date_tag = date = self.soup.select(".date")
        if(date_tag.__len__()):
            return date_tag[0].get_text()
        return ""
    def get_author(self):
        author_tag = self.soup.select(".byline__name")
        if(author_tag.__len__()):
            return author_tag[0].get_text().strip('By ')
        else:
            return ""
    def get_category(self):
        cat = self.soup.findAll("li", attrs = {'class' : 'selected'})
        if(cat.__len__()):
            return cat[0].span.text
        return ""
    def get_tagList(self):
        tagsCode = self.soup.findAll("ul", attrs = {'class' : 'tags-list'})
        if(tagsCode.__len__() == 1):
            tagsCode = tagsCode[0]
        elif(tagsCode.__len__() == 0):
            return []
        else:
            tagsCode = tagsCode[1]
        children = tagsCode.findChildren("li",recursive = False)
        return [child.text for child in children]
    def get_body(self):
        body = self.soup.find('div', attrs = {'class':'story-body__inner'})
        return str(body)
    def toS(self,l):
        s = l[0] + ','
        for tag in l[1:len(l) - 1]:
            s += tag + ','
        s += l[len(l) - 1]
        return s

    def submitToDb(self):
        t = str(int(time.time()))
        sql = "INSERT INTO articles2 (url,title,category,img,date,author,tag_list,body) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (self.id,self.title,self.category,self.img_url,self.date,self.author,self.tag_list,t)
        cursor.execute(sql,val)
        mydb.commit()
        f = open('html/'+t+'.html',"w")
        f.write(self.body)
        f.close()
        
   
     


    
    

if __name__=="__main__":
    url = 'https://www.bbc.com/news/technology-54091539'
    ins = ArticleScraper(url)
    ins.submitToDb()



    
















