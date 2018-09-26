# -*- coding: utf-8 -*-
from configparser import ConfigParser
from urllib.parse import quote
import socket
import os
import math
import urllib.request
from bs4 import BeautifulSoup
import time
import spider_search_page
import spider_paper
import pymysql


db = pymysql.connect("localhost", "root", "1234", "CrawlProject")
cursor = db.cursor()

def Crawl(currentpage,keyword):
    start = time.process_time()
    cf = ConfigParser()
    cf.read("Config.conf", encoding='utf-8')
    maxpage = cf.getint('base', 'maxpage')  # 最大页码
    searchlocation = cf.get('base', 'searchlocation')  # 搜索位置
    if os.path.exists('data-detail.txt') and currentpage == 0:
        print('存在输出文件，删除该文件')
        os.remove('data-detail.txt')

    # 构造不同条件的关键词搜索
    values = {
        '全文': 'qw',
        '主题': 'theme',
        '篇名': 'title',
        '作者': 'author',
        '摘要': 'abstract'
    }
    keywordval = str(values[searchlocation]) + ':' + str(keyword)
    index_url = 'http://search.cnki.com.cn/Search.aspx?q=' + quote(
        keywordval) + '&rank=&cluster=&val=&p='  # quote方法把汉字转换为encodeuri?
    print(index_url)

    # 获取最大页数
    html = urllib.request.urlopen(index_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    pagesum_text = soup.find('span', class_='page-sum').get_text()
    # maxpage = math.ceil(int(pagesum_text[7:-1]) / 15)
    # print(maxpage)
    cf = ConfigParser()
    cf.read("Config.conf", encoding='utf-8')
    cf.set('base', 'maxpage', str(maxpage))
    cf.write(open('Config.conf', 'w', encoding='utf-8'))

    for i in range(currentpage, maxpage):
        page_num = 15
        page_str_num = i * page_num
        page_url = index_url + str(page_str_num)
        print(page_url)
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                spider_search_page.get_paper_url(page_url)
                socket.setdefaulttimeout(100)  # 设置10秒后连接超时
                success = True
            except socket.error:
                attempts += 1
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break
            except urllib.error:
                attempts += 1
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break
        cf.set('base', 'currentpage', str(i))
        cf.write(open("Config.conf", "w", encoding='utf-8'))

    spider_paper.spider_paper(keyword)  # spider_paper补全文章信息
    end = time.process_time()
    print('Running time: %s Seconds' % (end - start))


if __name__ == '__main__':
    sql = "SELECT Category FROM Keyword"
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            print(row)
            Crawl(0,row)
    except:
        # 发生错误时回滚
        db.rollback()
        print("234567876543212345678765432")

