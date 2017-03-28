#coding:utf-8

import urllib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def getCommentCount(url):
    linkUrl = url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
    commentUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'.format(linkUrl)
    comments = requests.get(commentUrl).text.strip('var data=')
    jd = json.loads(comments)
    return jd['result']['count']['total']


def getNewsPage(url):
    urlContent = requests.get(url)
    urlContent.encoding = 'utf-8'
    soup = BeautifulSoup(urlContent.text, 'html.parser')
    time = soup.select('.time-source')[0].contents[0].strip() # get time
    # time = datetime.strftime(time, '%Y年%m月%d日%H:%M') # get time in special format
    source = soup.select('.time-source span a')[0].text # get source
    article = [] #get article
    for p in soup.select('#artibody p')[:-1]:
        article.append(p.text.strip())
    ''.join(article)
    editor  = soup.select('.article-editor')[0].text.strip('责任编辑：') #get editor
    commentCount = getCommentCount(url) # get commentCount
    return {"time":time, "source":source, "commentCount":commentCount, "article":article}






url = 'http://news.sina.com.cn/china/'
urlContent = requests.get(url)
urlContent.encoding = 'utf-8'
# print(urlContent.text)
soup = BeautifulSoup(urlContent.text, 'html.parser')
for news in soup.select(".news-item"):
    if len(news.select('h2')) > 0:
        print(news.select('.time')[0].text) #时间
        print(news.select('h2')[0].text) #标题
        print(news.select('a')[0]['href']) #连接
        #抓取页面内容
        detail = getNewsPage(news.select('a')[0]['href']) #未打印




