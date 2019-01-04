# -*- coding:utf-8 -*-
import re
import requests
import time
import os
import urllib3
urllib3.disable_warnings()
from selenium import webdriver
from bs4 import BeautifulSoup
import time
def get_one_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
    except Exception as er:
        print(er)


def get_pic_url(html):
    pic_urls = re.findall("data-src=\"(.*?jpg)", html, re.S)
    img_url = []
    for one_pic_url in pic_urls:
        img_url.append('http:' + one_pic_url)
    return img_url

def get_tianmao_pic_url(html):
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.select("#J_UlThumb ")[0].find_all(name='img', src=re.compile(".*?jpg"))
    img_url = []
    for one_pic_url in imgs:
        one_pic_url = str(one_pic_url.get('src'))
        one_pic_url = re.search('(.*?)jpg', one_pic_url)
        img_url.append('http:'+one_pic_url.group(0))
    return img_url

def get_item_pic_url(html):
    pic_urls = re.findall("background:url\((.*?jpg)", html, re.S)
    img_url = []
    for one_pic_url in pic_urls:
        img_url.append('http:' +one_pic_url)
    return img_url

def get_about_pic_url(url):
    browser = webdriver.Firefox()
    browser.get(url)
    sroll_cnt = 0
    while True:
        if sroll_cnt < 60:
            browser.execute_script('window.scrollBy(0, 500)')
            time.sleep(3)
            sroll_cnt += 1
        else:
            break
    sroll_cnt = 0
    html = browser.page_source
    img_url = []
    soup = BeautifulSoup(html, "html.parser")
    imgs =str(soup.select("#J_DivItemDesc ")[0].find_all(name='img', src=re.compile(".*?jpg"))[0])
    for img in re.findall("src=\"https:(.*?jpg)", imgs, re.S):
        img_url.append('http:'+img)
    browser.quit()
    return img_url

def get_tianmao_about_pic_url(url):
    browser = webdriver.Firefox()
    browser.get(url)
    sroll_cnt = 0
    while True:
        if sroll_cnt < 60:
            browser.execute_script('window.scrollBy(0, 500)')
            time.sleep(3)
            sroll_cnt += 1
        else:
            break
    sroll_cnt = 0
    html = browser.page_source
    img_url = []
    soup = BeautifulSoup(html, "html.parser")
    imgs =soup.findAll("img", {'class': 'img-ks-lazyload'})
    for img in imgs:
        img =str(img)
        for im in re.findall("src=\"https://(img.*?jpg)", img, re.S):
            img_url.append('http://'+im)
    browser.quit()
    return img_url


def write_to_file(img_prc_urls, img_item_urls, img_about_urls, title):
    title = title.replace(' ', '')
    title = title.replace('/', '')
    if not os.path.exists(title):
        os.mkdir(title)
    banerdir = title+u"\商品轮播图"
    sizedir = title + u"\商品尺码图"
    aboutdir = title + u"\商品详情图"
    if not os.path.exists(banerdir):
        os.mkdir(banerdir)
    if not os.path.exists(sizedir):
        os.mkdir(sizedir)
    if not os.path.exists(aboutdir):
        os.mkdir(aboutdir)
    n = 0
    for pic_url in img_prc_urls:
        pic = requests.get(pic_url)
        with open(banerdir + "/" + str(n) + '.jpg', 'wb') as f:
            f.write(pic.content)
        print(u'--第{}张图商品轮播图下载成功---'.format(str(n)))
        n += 1

    n = 0
    for pic_url in img_item_urls:
        pic = requests.get(pic_url)
        with open(sizedir + "/" + str(n) + '.jpg', 'wb') as f:
            f.write(pic.content)
        print(u'--第{}张图商品尺码图下载成功---'.format(str(n)))
        n += 1

    n = 0
    for pic_url in img_about_urls:
        pic = requests.get(pic_url)
        with open(aboutdir + "/" + str(n) + '.jpg', 'wb') as f:
            f.write(pic.content)
        print (u'--第{}张图商品详情图下载成功---'.format(str(n)))
        n += 1


def taoBao(url):
    html = get_one_html(url)
    img_item_urls = list(set(get_item_pic_url(html)))
    img_prc_urls = list(set(get_pic_url(html)))
    img_about_urls = list(set(get_about_pic_url(url)))
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text
    print title
    print img_prc_urls
    print img_item_urls
    print img_about_urls
    write_to_file(img_prc_urls, img_item_urls, img_about_urls, title)

def tianMao(url):
    html = get_one_html(url)
    img_prc_urls = list(set(get_tianmao_pic_url(html)))
    img_about_urls = list(set(get_tianmao_about_pic_url(url)))
    img_item_urls = list(set(get_item_pic_url(html)))
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text
    print title
    print img_prc_urls
    print img_about_urls
    print img_item_urls
    write_to_file(img_prc_urls, img_item_urls, img_about_urls, title)

if __name__ == '__main__':
    print u"请输入淘宝链接（必须是可以访问的淘宝链接）："
    url = raw_input()
    print u"程序运行中请等待三分钟！"
    # url = "https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4011-14869619373.62.3f52187bvAg1Vp&id=537772885220&rn=b8fde60fb004941a35edbca8eaa586d8&abbucket=7&sku_properties=1627207:6071353"
    if re.match(".*?tmall", url):
        tianMao(url)
    else:
        taoBao(url)