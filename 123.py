#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   123.py    
@Contact :   www.rainzy.com/blog
@License :   (C)Copyright 2020

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/14 19:57   Rainzy      1.0         None
'''

import xlsxwriter
import xlrd
import xlwt
import openpyxl

if __name__ == '__main__':
    with xlsxwriter.Workbook('TCM_I2T.xlsx') as writer:
        sheet = writer.add_worksheet('I2T')
        sheet.write_row(0, 1, 'targe')
