import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
from string import punctuation
from selenium import webdriver
from collections import OrderedDict


def getTable(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)[0][:200]
    page = BeautifulSoup(html)
    links = []
    tags = page.findAll('a', {"class": "image"})
    for tag in tags:
        links.append("https://en.wikipedia.org" + str(tag['href']) + "\n")
    imageurls = []
    for i in range(50):
        imgpage = BeautifulSoup(requests.get(links[i]).content)
        img = imgpage.find("div", {"id": "file"})
        img = img.find("img")
        img = img["src"]
        imageurls.append(img)
    df_list['Image'] = imageurls
    df_list['Image'] = 'https:' + df_list['Image'].astype(str)
    df_list['Title'] = [row[0] for row in df_list['Title'].str.split(',')]
    df_list['File'] = df_list['Title'].str.replace(rf'[{punctuation}]', '').str.replace(" ", "-")
    df_list['File'] = '../assets/' + df_list['File'].astype(str) + '.jpg'
    return df_list.iloc[0:200][['Title', 'File', 'Image']].drop_duplicates(subset='Title', keep="last").reset_index().drop(['index'], axis=1)

def getDataTable(url):
    html = requests.get(url).content
    df = pd.read_html(html)[0]
    df['Title'] = [row[0] for row in df['Title'].str.split(',')]
    df['Year'] = [row[-1] for row in df['Year'].str.split(' ')]
    df['Year'] = [row[0] for row in df['Year'].str.split('–')] 
    df['Year'] = [row[-1] for row in df['Year'].str.split('.')]
    df['Year'] = [row[0] for row in df['Year'].str.split('-')]
    df['Year'] = [row[-1] for row in df['Year'].str.split('/')]
    df['Current location'] = [row[0] for row in df['Current location'].str.split(',')]
    df = df.drop_duplicates(subset='Title', keep="last").drop(['No.'], axis=1)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df['Current location'])

def downloadImage(df):
    for index, row in df.iterrows():
        urllib.request.urlretrieve(row['Image'], row['File'])

def handleArtistPage(url):
    html = requests.get(url).content
    page = BeautifulSoup(html)
    tags = page.findAll('li')
    if len(tags) == 0:
        return [url]
    links = []
    for tag in tags:
        a = tag.find('a')
        links.append(url.split("index")[0] + a['href'])
    return(links)

def handleArtPages(links):
    browser = webdriver.Firefox('/usr/local/bin')
    lst = []
    for link in links:
        browser.get(link)
        tags = browser.find_elements_by_tag_name('img')
        for tag in tags:
            src = tag.get_attribute('src')
            if "preview" in src:
                lst.append(src)
    lst = list(OrderedDict.fromkeys(lst))
    browser.close()
    print(lst)
    


handleArtPages(handleArtistPage("https://www.wga.hu/html_m/g/gogh_van/01/index.html"))
#getDataTable("https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh")

