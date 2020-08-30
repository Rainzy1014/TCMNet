#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TCMSP_Spider.py    
@Contact :   www.rainzy.com/blog
@License :   (C)Copyright 2020

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/16 10:56   Rainzy      1.0         None
'''
import os

import requests
import urllib.parse  # urllib用以解码中药材名称，是否需要见具体需求
from bs4 import BeautifulSoup
import re
import xlsxwriter
import xlrd
import xlwt
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class get_drug_target(object):

    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }
        self.base_url = 'https://tcmspw.com/tcmspsearch.php?'
        self.browser = webdriver.Chrome()
        # print(self.base_url)

    def get_url(self, drug):
        # 下面注释的是中文解码的过程
        # drug_decode = urllib.parse.quote(drug)
        # url = self.base_url+'qs=herb_all_name&q='+drug_decode+'&token=f8abf58ec1d6b214e0d6ca4ec94ee7d3'
        # 下面是不解码
        url = self.base_url + 'qs=herb_all_name&q=' + drug + '&token=745598c3dd27ba93cf48a4d3ec5df794'

        self.browser.get(url)
        # print(self.browser.page_source)
        return self.browser.page_source

    def search_drug_url(self, data):
        soup = BeautifulSoup(data, 'lxml')
        # 寻找javascript中的数据
        drug_url1 = soup.find_all('script')
        drug_url1 = str(drug_url1)
        # 获取英文名
        drug_name1 = re.search(r'"herb_en_name":"(.*?)"', drug_url1).group(1)
        # 将英文名之间的空格替换为 %20
        drug_name2 = drug_name1.replace(' ', '%20')
        # 获取url地址
        drug_url2 = re.search(r"href='(.+)'", drug_url1).group(1)
        # 拼接url
        combined_url = 'http://tcmspw.com/' + drug_url2.split('$')[0] + drug_name2 + drug_url2.split('}')[1]
        return combined_url

    def run(self):

        # excel_path = "TCM_Data.xlsx"
        # workbook = xlrd.open_workbook(excel_path)
        # sheet=workbook.sheets()[0]
        # drug_list = []
        # nrows = sheet.nrows  # 行数
        # # 根据sheet索引或者名称获取sheet内容
        # # sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        # for rownum in range(0, nrows):
        #     # print(sheet.row_values(rownum)[1])
        #     temp_drugArray =  sheet.row_values(rownum)[1].split('，')
        #     # print(temp_drugArray)
        #     for tempdrug in temp_drugArray:
        #         if not ( tempdrug in drug_list):
        #             drug_list.append(tempdrug)
        # print(drug_list)
        #
        #
        # with xlsxwriter.Workbook('TCM_H2I.xlsx') as writer:
        #     sheet = writer.add_worksheet('H2I')
        #     for index, drug in enumerate(drug_list):
        #         data = self.get_url(drug)
        #         combined_url = self.search_drug_url(data)
        #         print(combined_url)
        #         self.browser.get(combined_url)
        #         # print(self.browser.page_source)
        #
        #         ingredient_data = self.get_ingredient(combined_url)
        #         ingredientlist = []
        #         # print(items)
        #         for item in ingredient_data:
        #             modid = 'MOL' + item[0]
        #             ingredientlist.append(modid)
        #         print("ingredient_data:", ingredientlist)
        #         sheet.write_row(index, 1, ingredientlist)
        #         sheet.write(index, 0, drug_list[index])
        # writer.close()

        excel_path = "TCM_H2I.xlsx"
        workbook = xlrd.open_workbook(excel_path)
        sheet = workbook.sheets()[0]
        ingredient_list = []
        nrows = sheet.nrows  # 行数

        for rownum in range(0, nrows):
            # print(sheet.row_values(rownum))
            temp_drugArray = sheet.row_values(rownum)[1:]
            # print(temp_drugArray)
            for tempdrug in temp_drugArray:
                if not (tempdrug in ingredient_list):
                    ingredient_list.append(tempdrug)
        print(len(ingredient_list))
        # input()
        # 写入相关靶标

        with xlsxwriter.Workbook('TCM_I2T.xlsx') as writer:
            sheet = writer.add_worksheet('I2T')
            # sheet.write_row(0, 1, 'targetlist')
            # input()

            workbook1 = xlrd.open_workbook('TCM_I2T.xlsx')
            readsheet = workbook1.sheets()[0]
            #
            for index, molid in enumerate(ingredient_list):
                print('````````````````````````````````````````')
                target_data = self.getRelatedTarget(molid)
                targetlist = []

                print(index + 1)
                for item in target_data:
                    targetlist.append(item)
                print("Target_data:", targetlist)
                if not len(targetlist) == 0:
                    sheet.write_row(index, 1, targetlist)
                    sheet.write(index, 0, ingredient_list[index])
                else:
                    sheet.write_row(index, 1, ['N/A'])
                    sheet.write(index, 0, ingredient_list[index])

        writer.close()

        self.browser.close()

    def getRelatedTarget(self, molid):

        common_url = "https://tcmspw.com/molecule.php?qn="
        url = common_url + molid[3:]
        print(url)
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        if len(soup.select("#kendo_target > div.k-pager-wrap.k-grid-pager.k-widget > a:nth-child(5)")) < 1:
            return []

        pagenumber = soup.select("#kendo_target > div.k-pager-wrap.k-grid-pager.k-widget > a:nth-child(5)")[0][
            'data-page']

        # print(pagenumber)
        itemnumberstr = soup.select('#kendo_target > div.k-pager-wrap.k-grid-pager.k-widget > span')[0].contents[0]
        itemnumber = int(itemnumberstr.split(' ')[4])
        print(itemnumber)

        # pattern = re.compile('<tr.*?<div id="kendo_target">(.*?)</div>*?</tr>')
        # temp = re.findall(pattern, self.browser.page_source)
        # if len(temp)!=0:
        #     return []

        # self.browser.close()
        pattern = re.compile('<tr.*?data-uid=.*?target.php.*?>(.*?)</a></td><td role="gridcell">.*?</a></td>*?</tr>')
        items = re.findall(pattern, self.browser.page_source)
        # print(items)
        tempitemnumber = len(items)
        pnumber = int(pagenumber)
        while (pnumber - 1 != 0) and (tempitemnumber < itemnumber):
            nextpage = self.browser.find_element_by_css_selector(
                '#kendo_target > div.k-pager-wrap.k-grid-pager.k-widget > a:nth-child(4)')
            nextpage.click()
            pattern = re.compile(
                '<tr.*?data-uid=.*?target.php.*?>(.*?)</a></td><td role="gridcell">.*?</a></td>*?</tr>')
            if pnumber - 1 > 1:
                temp_items = re.findall(pattern, self.browser.page_source)[:10]
                print(temp_items)
                items += temp_items
                tempitemnumber += len(temp_items)
                pnumber -= 1
            else:
                temp = itemnumber - tempitemnumber
                temp_items = re.findall(pattern, self.browser.page_source)[:temp]
                # print(temp_items)
                items += temp_items
                tempitemnumber += len(temp_items)
            # print(tempitemnumber)
        return items

    def get_ingredient(self, url):

        self.browser.get(url)
        # print(self.browser.page_source)
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        # 一共10个script
        pagenumber = soup.find(title='Go to the last page')['data-page']
        itemnumberstr = soup.find(class_='k-pager-info').contents[0]
        itemnumber = int(itemnumberstr.split(' ')[4])
        print(itemnumber)
        # self.browser.close()
        pattern = re.compile('<tr.*?data-uid=.*?>MOL(.*?)</td><td.*?><a href="(.*?)">(.*?)</a>.*?</tr>')
        items = re.findall(pattern, self.browser.page_source)[:15]
        tempitemnumber = len(items)
        pnumber = int(pagenumber)
        while (pnumber - 1 != 0) and (tempitemnumber < itemnumber):
            nextpage = self.browser.find_element_by_css_selector(
                '#grid > div.k-pager-wrap.k-grid-pager.k-widget > a:nth-child(4)')
            nextpage.click()
            pattern = re.compile('<tr.*?data-uid=.*?>MOL(.*?)</td><td.*?><a href="(.*?)">(.*?)</a>.*?</tr>')
            if pnumber - 1 > 1:
                temp_items = re.findall(pattern, self.browser.page_source)[:15]
                # print(temp_items)
                items += temp_items
                tempitemnumber += len(temp_items)
                pnumber -= 1
            else:
                temp = itemnumber - tempitemnumber
                temp_items = re.findall(pattern, self.browser.page_source)[:temp]
                # print(temp_items)
                items += temp_items
                tempitemnumber += len(temp_items)
            # print(tempitemnumber)
        return items


if __name__ == '__main__':
    function = get_drug_target()
    function.run()
