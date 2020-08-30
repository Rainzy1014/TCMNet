#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SpiderDemo.py    
@Contact :   www.rainzy.com/blog
@License :   (C)Copyright 2020

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/16 13:03   Rainzy      1.0         None
'''
import requests
import re
import json
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get("https://tcmspw.com/tcmspsearch.php?qs=herb_all_name&q=麻黄&token=745598c3dd27ba93cf48a4d3ec5df794")
    print(browser.page_source)
finally:
    browser.close()