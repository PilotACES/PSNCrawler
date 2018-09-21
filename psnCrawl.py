#!/usr/bin/env python
# encoding: utf-8
'''
@author: Johnny Mo
@contact: motorolasoap@gmail.com
@file: psnCrawl.py
@time: 2018/9/22 1:17
@desc:
'''

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

"""
从PSN获取游戏列表
Parameters:
    page - PSN商店页数，默认为第一页
Returns:
    game_list - 游戏列表
Modify:
    2018-09-21
"""
def get_gameInfo(url):
    sesson = requests.Session()
    target_url = 'https://store.playstation.com/' + str(url)
    target_header = {'upgrade-insecure-requests': '1',
                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                     'if-none-match': '53e87-V+GaRKPoAIWVQJnTCbtEMmCTw1Q',
                     'cache-control': 'max-age=0',
                     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                     'accept-encoding': 'accept-encoding',
                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                     }
    target_response = sesson.get(url = target_url, headers = target_header)
    target_response.encoding = 'utf-8'
    target_html = target_response.text
    page1_game_list = BeautifulSoup(target_html, 'lxml')
    page2_game_list = page1_game_list.find_all('div', class_=re.compile('grid-cell grid-cell--game'))
    games_list = []

    for gameObj in page2_game_list:
        dom = etree.HTML(str(gameObj))
        gameDiv = dom.xpath('//span[@title]/@title')
        gamePlatform = dom.xpath("//div[@class='grid-cell__left-detail grid-cell__left-detail--detail-1']/text()")
        gameType = dom.xpath("//div[@class='grid-cell__left-detail grid-cell__left-detail--detail-2']/text()")
        gameFullPrice = dom.xpath("//h3[@class='price-display__price']/text()")
        gameDiscountPrice = dom.xpath("//div[@class='price-display__price--is-plus-upsell']/text()")

        if len(gameDiv) == 0:
            gameDiv=['暂无名称']

        if len(gamePlatform) == 0:
            gamePlatform=['平台未定']

        if len(gameType) == 0:
            gameType=['无']

        if len(gameFullPrice) == 0:
            gameFullPrice=['暂无售价']
            gameDiscountPrice=['暂无售价']

        if (len(gameDiscountPrice) == 0 and len(gameFullPrice)>0):
            gameDiscountPrice=gameFullPrice.copy()

        gameInfo = {'gameName': str(gameDiv[0]),
                    'gamePlatform': str(gamePlatform[0]),
                    'gameType': str(gameType[0]),
                    'gameFullPrice': str(gameFullPrice[0]),
                    'gameDiscountPrice': str(gameDiscountPrice[0])}
        games_list.append(gameInfo)
        print("==================== %s ====================\n" % str(gameDiv[0]))
        print("發售平台: %s \n" % str(gamePlatform[0]))
        print("上架類型: %s \n" % str(gameType[0]))
        print("發售價格: %s \n" % str(gameFullPrice[0]))
        print("折扣價格: %s \n" % str(gameDiscountPrice[0]))
        print("\n")
    return games_list

"""
    获取最大页数
"""
def getMaxPage(url):
    sesson = requests.Session()
    target_url = 'https://store.playstation.com/' + str(url)
    target_header = {'upgrade-insecure-requests': '1',
                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                     'if-none-match': '53e87-V+GaRKPoAIWVQJnTCbtEMmCTw1Q',
                     'cache-control': 'max-age=0',
                     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                     'accept-encoding': 'accept-encoding',
                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                     }
    target_response = requests.get(url=target_url, headers=target_header)
    target_response.encoding = 'utf-8'
    target_html = target_response.text
    page1_game_list = BeautifulSoup(target_html, 'lxml')
    finalPageArrow = page1_game_list.find("a", class_=re.compile('paginator-control__end paginator-control__arrow-navigation'))
    maxPageURL = finalPageArrow.get('href')
    maxPageStr = re.findall(r'\/[0-9]+', maxPageURL)
    if len(maxPageStr) > 0:
        maxPage = re.findall('[0-9]+', maxPageStr[0])
        if len(maxPage) > 0:
            return int(str(maxPage[0]))
    return 1

if __name__ == '__main__':
    txt_name = "PSNGames.txt"
    fName = open(txt_name, 'w', encoding='utf-8')
    max = getMaxPage('zh-hant-hk/grid/STORE-MSF86012-GAMESALL/1?smcid=hk-cht_ps%3Acom_header') + 1
    for page_index in range(1, max):
        url = "zh-hant-hk/grid/STORE-MSF86012-GAMESALL/"+ str(page_index) +"?smcid=hk-cht_ps%3Acom_header"
        games_list = get_gameInfo(url)
        fName.write("######################################  第%d页  ######################################\n" % page_index)
        fName.flush()
        for gamesInfo in games_list:
            fName.write("==================== %s ====================\n" % str(gamesInfo['gameName']))
            fName.write("發售平台: %s \n" % str(gamesInfo['gamePlatform']))
            fName.write("上架類型: %s \n" % str(gamesInfo['gameType']))
            fName.write("發售價格: %s \n" % str(gamesInfo['gameFullPrice']))
            fName.write("折扣價格: %s \n" % str(gamesInfo['gameDiscountPrice']))
            fName.write("\n")
            fName.flush()
    fName.close()








