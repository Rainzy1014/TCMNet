#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TCMNet.py
@Contact :   www.rainzy.com/blog
@License :   (C)Copyright 2020

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/15 15:36   Rainzy      1.0         None
'''
import xlrd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher


class TCMNetX:
    def __init__(self, vertexs, edges, relationships):
        self.vectors = vertexs
        self.edges = edges
        self.relationships = relationships
        self.graph = Graph('bolt://localhost:7687', username='neo4j', password='123')

    def createNode(self, nodetype, nodename):

        return



    def run(self):
        return

    def readNodesToList(self, excel_path):
        workbook = xlrd.open_workbook(excel_path)
        sheet = workbook.sheets()[0]
        nodelist = []
        nrows = sheet.nrows  # 行数
        for rownum in range(0, nrows):
            print(sheet.row_values(rownum)[0])
            nodelist.append(sheet.row_values(rownum)[0])
        return nodelist



if __name__ == '__main__':

    vertexs = []
    edges = []
    relationships = []
    net = TCMNet(vertexs, edges, relationships)
    # read nodes and write into neo4j
    # prescriptionList = net.readNodesToList("TCM_Data.xlsx")
    # print(prescriptionList)





    workbook = xlrd.open_workbook("TCM_Data.xlsx")
    sheet = workbook.sheets()[0]
    prescriptionList = []
    prescriptionNameList = []
    herbList = []
    herbNameList =[]
    nrows = sheet.nrows  # 行数
    for rownum in range(0, nrows):
        print(sheet.row_values(rownum)[0])
        a = Node('Prescription', name = sheet.row_values(rownum)[0])
        net.graph.create(a)
        prescriptionList.append(a)
        prescriptionNameList.append(a['name'])
        print(a.identity)
        temp_drugArray = sheet.row_values(rownum)[1:]
        for tempdrug in temp_drugArray:
            if tempdrug not in herbNameList and tempdrug != '':
                b = Node('Herb', name=tempdrug)
                net.graph.create(b)
                herbList.append(b)
                herbNameList.append(b['name'])
                print('name1:' + str(b.identity) + b['name'])
                r = Relationship(a, 'P2H', b, name='P2H')
                net.graph.create(r)
            else:
                for item in herbList:
                    if item['name'] == tempdrug:
                        print('name2:' + str(item.identity) + tempdrug)
                        r = Relationship(a, 'P2H', item, name='P2H')
                        net.graph.create(r)

    workbook = xlrd.open_workbook("TCM_H2I.xlsx")
    sheet = workbook.sheets()[0]
    prescriptionList = []
    ingredientList = []
    ingredientNameList = []
    nrows = sheet.nrows  # 行数
    for rownum in range(0, nrows):
        print(sheet.row_values(rownum)[0])

        for item in herbList:
            if item['name'] == sheet.row_values(rownum)[0]:
                a = item
        tempArray = sheet.row_values(rownum)[1:]
        for temp in tempArray:
            if temp not in ingredientNameList and temp != '':
                b = Node('Ingredient', name=temp)
                net.graph.create(b)
                ingredientList.append(b)
                ingredientNameList.append(b['name'])
                print('name1:' + str(b.identity) + b['name'])
                r = Relationship(a, 'H2I', b, name='H2I')
                net.graph.create(r)
            else:
                for item in ingredientList:
                    if item['name'] == temp:
                        print('name2:' + str(item.identity) + temp)
                        r = Relationship(a, 'H2I', item, name='H2I')
                        net.graph.create(r)

    workbook = xlrd.open_workbook("TCM_I2T.xlsx")
    sheet = workbook.sheets()[0]
    targetList = []
    targetNameList = []
    nrows = sheet.nrows  # 行数
    for rownum in range(0, nrows):
        print(sheet.row_values(rownum)[0])

        for item in ingredientList:
            if item['name'] == sheet.row_values(rownum)[0]:
                a = item
        tempArray = sheet.row_values(rownum)[1:]
        for temp in tempArray:
            if temp not in targetNameList and temp != '' and temp !='N/A':
                b = Node('target', name=temp)
                net.graph.create(b)
                targetList.append(b)
                targetNameList.append(b['name'])
                print('name1:' + str(b.identity) + b['name'])
                r = Relationship(a, 'H2I', b, name='H2I')
                net.graph.create(r)
            else:
                for item in targetList:
                    if item['name'] == temp:
                        print('name2:' + str(item.identity) + temp)
                        r = Relationship(a, 'I2T', item, name='I2T')
                        net.graph.create(r)


















