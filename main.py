from  scraper import *
import requests
from bs4 import BeautifulSoup
import time



def cat_scrap(catUrl):
    root = 'https://www.bbc.com'
    response = requests.get(root + catUrl)
    html = response.content
    soup = BeautifulSoup(html,"html.parser")

    latest = soup.find('div',attrs = {'class':'lx-stream__feed'})
    articles = latest.findAll('article')
    for article in articles:
        time.sleep(1)
        try:
            url = root + article.header.div.h3.a['href']
        except:
            continue

        
        ins = ArticleScraper(url)
        try:
            ins.submitToDb()
        except:
            continue


if __name__ == "__main__":
    root = 'https://www.bbc.com'
    category = "https://www.bbc.com/news/world"
    
    response = requests.get(root+'/news')
    html = response.content
    soup = BeautifulSoup(html,"html.parser")
    cats = soup.find('nav',{'class':'nw-c-nav__wide'}).ul.findAll('li')

    for li in cats:
        try:
            if(li.get_text() == 'Video'):
                continue
            cat_scrap(li.a['href'])
        except:
            continue

    """
    
    """