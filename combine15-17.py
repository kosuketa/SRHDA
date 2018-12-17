
# coding: utf-8

# In[4]:


import pandas as pd
from pprint import pprint
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import csv
import copy
from os import listdir
import re

HOME='/home/is/kosuke-t'


# In[5]:


def loadCsv2Df(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df
def saveDf2Csv(filename, df):
    df.to_csv(filename, encoding='utf-8')

def combineData(lang): 
    global HOME
    datadir = HOME+'/data/SrcRefHypRawDA/'
    data2017 = datadir + 'newstest2017.'+lang+'.csv'
    data2016 = datadir + 'newstest2016.'+lang+'.csv'
    data2015 = datadir + 'newstest2015.'+lang+'.csv'
    return pd.concat([pd.concat([loadCsv2Df(data2017).drop(['RawDA'],axis=1), loadCsv2Df(data2016).drop(['RawDA'],axis=1)], axis=0), loadCsv2Df(data2015)], axis=0)


# In[6]:


DF = {} #key:language
WriteDir=HOME+'/data/SrcRefHypRawDA'
for lang in ['cs-en', 'de-en', 'fi-en', 'ru-en']:
    DF[lang] = combineData(lang)
    saveDf2Csv(WriteDir+'/newstest2015-2017.'+lang+'.csv', DF[lang])


# In[8]:


DF['de-en']

