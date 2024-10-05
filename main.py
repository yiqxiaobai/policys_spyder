# -*- coding:utf-8 -*-
"""
Desc: This is Code Desc
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import pickle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
#
# # 1. 发送请求, 获取疫情首页内容
# response = requests.get('https://www.shggzy.com/zcfgzhfg', headers=headers)
# if response.status_code == 200:
#     pass
# else:
#     print(f"Failed to retrieve the page. Status code: {response.status_code}")
#
# home_page = response.content.decode()
#
# # 获取每一页主页的网址
# def get_home_page(url):
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         pass
#     else:
#         print(f"Failed to retrieve the page. Status code: {response.status_code}")
#         time.sleep(5)
#         return get_home_page(url)
#     home_page = response.content.decode()
#     time.sleep(5)
#     return home_page
#
#
# home_pages = []
# urls = [f"https://www.shggzy.com/zcfgzhfg_{i + 1}.jhtml" for i in range(7)]
#
#
# for url in urls:
#     home_pages.append(get_home_page(url))
#     print(0)
#
# print(home_pages)
# with open(r"data/home_pages.pkl", "wb") as file:
#     pickle.dump(home_pages, file)


# 2. 从综合法律法规专栏首页开始, 提取每页所有政策的超链接
with open("data/home_pages.pkl", "rb") as file:
    home_pages = pickle.load(file)
    # print(home_pages)

source_link = "https://www.shggzy.com"


def get_everypages_links(home_page):
    soup = BeautifulSoup(home_page, 'lxml')
    script = soup.find_all("span", class_="cs-span2", style="width: 86%;")
    script_links = [source_link + span_.parent.attrs["onclick"][13:-2] for span_ in script]
    if script_links:
        return script_links
    else:
        return get_everypages_links(home_page)


hyperlink_addresses = [get_everypages_links(home_page) for home_page in home_pages]


# print(hyperlink_addresses)


# 3. 从政策页面提取政策内容
def get_policy(policy_url):
    # 2. 发送请求, 获取政策内容
    response = requests.get(policy_url, headers=headers)
    # print(response)
    if response.status_code == 200:
        policy_page = response.content.decode()
        # print(policy_page)
        # 3. 使用BeautifulSoup提取数据
        soup = BeautifulSoup(policy_page, 'lxml')
        # 提取一级标题
        script = soup.find_all("div", class_="content-box")[0]
        # print(len(script))
        policy_title = script.h2.string
        # 提取正文内容
        content = script.div.text.strip()
        # 写入文件
        with open(rf'./data/policy_files/{policy_title}.txt', mode='w', encoding="utf-8") as file:
            file.write(content)
    else:
        time.sleep(5)
        get_policy(policy_url)


# hyperlink_addressessh是个二维列表，综合法律法规专栏里，每页的目录页是一个列表，每个列表是每页的政策页的地址
for every_pages in hyperlink_addresses:
    for policy_page in every_pages:
        get_policy(policy_page)
        time.sleep(5)
