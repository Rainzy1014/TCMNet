#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Medicine.py
@Contact :   www.rainzy.com/blog
@License :   (C)Copyright 2020

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/15 16:40   Rainzy      1.0         None
'''

# import lib





class Prescription():
    def __init__(self, name, herbs, herb_number):
        self.name = name
        self.herbs = herbs
        self.herb_number = herb_number

    def getName(self):
        return self.name

    def getHerbs(self):
        return self.herbs

    def getHerbsNumber(self):
        return self.herb_number

class Herb():
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

class Ingredient():
    def __init__(self, molid, name, targets):
        self.molid = molid
        self.name = name
        self.targets = targets

    def getName(self):
        return self.name

    def getMolID(self):
        return self.molid

    def getTargets(self):
        return self.targets

class Target():
    def __init__(self, name, gene):
        self.name = name
        self.ingredients = gene

    def getName(self):
        return self.name

    def getGene(self):
        return self.gene

class Gene():
    def __init__(self, name):
        self.name = name
        # self.ingredients = ingredients

    def getName(self):
        return self.name

    # def getIngredients(self):
    #     return self.ingredients