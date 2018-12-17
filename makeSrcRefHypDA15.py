
# coding: utf-8

# In[1]:


import pandas as pd
from pprint import pprint
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import csv
import copy
from os import listdir
import re


# In[11]:


HOME='/home/is/kosuke-t'
DIR=HOME+'/script'
#DataDir16=HOME+'/data/DAseg-wmt-newstest2016'
DataDir15=HOME+'/data/DAseg-wmt-newstest2015'
#languages16 = ['cs-en', 'de-en', 'fi-en', 'ro-en', 'ru-en', 'tr-en']
languages15 = ['cs-en', 'de-en', 'fi-en', 'ru-en']

# srcs16 = {}
# refs16 = {}
# hyps16 = {}
# DAs16 = {}
srcs15 = {}
refs15 = {}
hyps15 = {}
DAs15 = {}
# for l in languages16:
#     srcs16[l] = DataDir16 + '/DAseg.newstest2016.source.' + l
#     refs16[l] = DataDir16 + '/DAseg.newstest2016.reference.' + l
#     hyps16[l] = DataDir16 + '/DAseg.newstest2016.mt-system.' + l
#     DAs16[l] = DataDir16 + '/DAseg.newstest2016.human.' + l
for l in languages15:
    srcs15[l] = DataDir15 + '/DAseg.newstest2015.source.' + l
    refs15[l] = DataDir15 + '/DAseg.newstest2015.reference.' + l
    hyps15[l] = DataDir15 + '/DAseg.newstest2015.mt-system.' + l
    DAs15[l] = DataDir15 + '/DAseg.newstest2015.human.' + l


# In[20]:


def loadCsv2Df(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df
def saveDf2Csv(filename, df):
    df.to_csv(filename, encoding='utf-8')

def loadfile(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as r:
        data = r.read().split('\n')
        if data[-1] == '':
            data.pop(-1)
    return data

def makeDF16(lang):
    global srcs16, refes16, hyps16, DAs16
    SRC = loadfile(srcs16[lang])
    REF = loadfile(refs16[lang])
    HYP = loadfile(hyps16[lang])
    DA = loadfile(DAs16[lang])
    return pd.DataFrame({'SRC':SRC, 'REF':REF, 'HYP':HYP, 'Z-DA':DA})

def makeDF15(lang):
    global srcs15, refes15, hyps15, DAs15
    SRC = loadfile(srcs15[lang])
    REF = loadfile(refs15[lang])
    HYP = loadfile(hyps15[lang])
    DA = loadfile(DAs15[lang])
    return pd.DataFrame({'SRC':SRC, 'REF':REF, 'HYP':HYP, 'Z-DA':DA})


# In[21]:


DF16 = {} #key:language
DF15 = {}
WriteDir=HOME+'/data/SrcRefHypRawDA'
# for lang in languages16:
#     DF16[lang] = makeDF16(lang)
#     saveDf2Csv(WriteDir+'/newstest2016.'+lang+'.csv', DF16[lang])

for lang in languages15:
    DF15[lang] = makeDF15(lang)
    saveDf2Csv(WriteDir+'/newstest2015.'+lang+'.csv', DF15[lang])


# In[22]:


#DF16['de-en']

