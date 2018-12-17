
# coding: utf-8

# In[2]:


import pandas as pd
from pprint import pprint
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import csv
import copy
from os import listdir
import re


# ### Directory names (need to be fixed for your environment)  
# Variables to be fixed:  
# HOME, DIR(script DIR), DataDir, HypDir, languages, DAFiles  
#   
# data must be in the same form of 2017 DA data

# In[32]:


HOME='/home/is/kosuke-t'
DIR=HOME+'/script'
DataDir=HOME+'/data/wmt16-submitted-data/txt'
HypDir=DataDir+'/system-outputs/newstest2016'

languages = ['cs-en', 'de-en', 'fi-en', 'ro-en', 'ru-en', 'tr-en']
systems = {} #key:language, value:MTsystem
hyps= {} #key:language, value:dic→key:MTsystem
srcs = {} #key:language, value:filename
refs = {} #key:language, value:filename
for lang in languages:
    systems[lang] = [re.sub(r'(newstest2016\.)|\.[0-9]+\.'+lang, '', s) for s in listdir(HypDir+'/'+lang)]
    hyps[lang] = {}
    
    for f in listdir(HypDir+'/'+lang):
        for system in systems[lang]:
            fpattern = 'newstest2016.'+system+'.'+lang
            ftmp = re.sub(r'[0-9]+\.'+lang, lang, f)
            if re.match(fpattern, ftmp):
                hyps[lang][system]= HypDir+'/'+lang+'/'+ f
    
    for f in listdir(DataDir+'/sources'):
        if re.search('\.en', f):
            continue
        s1 = re.sub('-', '', lang)+'-src.'+re.sub('-en', '', lang)
        if re.search(s1, f):
            srcs[lang]=DataDir+'/sources/'+f
    
    for f in listdir(DataDir+'/references'):
        if not re.search('\.en', f):
            continue
        s1 = re.sub('-', '', lang)+'-ref.en'
        if re.search(s1, f):
            refs[lang]=DataDir+'/references/' + f          

DAfiles = {}
for lang in languages:
    DAfiles[lang]= HOME+'/data/DAsys-wmt-newstest2016/' +          'ad-seg-scores-' + lang + '.csv'  

#pprint(systems['de-en'])
pprint(hyps)


# ### Collecting data from csv 

# In[34]:


def loadCsv2Df(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    return df
def saveDf2Csv(filename, df):
    df.to_csv(filename, encoding='utf-8')

## return data type:dicionary
## key:system name, 
## value: list = [SID, RAW.SCR, Z.SCR, N]
def loadDA(filename):
    data = {}
    f = open(filename, mode='r', newline='')
    csvObj = csv.reader(f)
    flag = 0
    for row in csvObj:
        if flag == 0:
            flag = 1
            continue
        sys = row[0].split()[0]
        if sys not in data:
            data[sys] = []
        data[sys].append(row[0].split()[1:])
        data[sys][-1][0] = int(data[sys][-1][0])
        data[sys][-1][1] = float(data[sys][-1][1])
        data[sys][-1][2] = float(data[sys][-1][2])
        data[sys][-1][3] = int(data[sys][-1][3])

    f.close()

    return data

# sort DA data from loadDA() by SID in ascending
# retuning DATA = [list(SID), list(RawScore), list(Z-Score), list(NTimes)]
def getDA(filename, system):
    data = sorted(loadDA(filename)[system], key=itemgetter(0))
    DATA = [[data[i][j] for i in range(len(data))] for j in range(4)]
    return DATA

def loadfile(filename, SIDs):
    data = []
    with open(filename, mode='r', encoding='utf-8') as r:
        datatmp = r.read().split('\n')
        if datatmp[-1] == '':
            datatmp.pop(-1)
        data = [datatmp[id-1] for id in SIDs]
    return data

#for the specified language, make a dataframe that has [src, ref, hyp, RawDA] as collumn 
def makeDF(lang):
    global systems, srcs, refs, hyps, DAfiles
    df = pd.DataFrame()
    for system in systems[lang]:
        try:
            DAdata = getDA(DAfiles[lang], system)
            Src = loadfile(srcs[lang], DAdata[0])
            Ref = loadfile(refs[lang], DAdata[0])
            Hyp = loadfile(hyps[lang][system], DAdata[0])
        except:
            print('[{},{}] does not exist in the DA csv'.format(lang, system))
            continue
        
        tmp_df = pd.DataFrame({'SRC':Src, 'REF':Ref, 'HYP':Hyp, 'Z-DA':DAdata[2], 'RawDA':DAdata[1]})
        df = pd.concat([df, tmp_df], axis=0)
    return df    


# ### make DF and writedown to CSV

# In[35]:


DF = {} #key:language
WriteDir=HOME+'/data/SrcRefHypRawDA'
for lang in languages:
    DF[lang] = makeDF(lang)
    saveDf2Csv(WriteDir+'/newstest2016.'+lang+'.csv', DF[lang])


# In[36]:


total = 0
for lang in languages:
    total += len(DF[lang])
    print(lang,len(DF[lang]))
    
print('total number of sentences : {}'.format(total))


# In[37]:


DF['de-en']


# ### Combine 2015, 2016 data together

# In[43]:


def combineData(lang):
    global HOME
    datadir = HOME+'/data/SrcRefHypRawDA/'
    data2017 = datadir + 'newstest2017.'+lang+'.csv'
    data2016 = datadir + 'newstest2016.'+lang+'.csv'
    data2015 = datadir + 'newstest2015.'+lang+'.csv'
    return pd.concat([pd.concat([loadCsv2Df(data2017).drop(['RawDA'],axis=1), loadCsv2Df(data2016).drop(['RawDA'],axis=1)], axis=0), loadCsv2Df(data2015)], axis=0)
    


# In[44]:





# In[46]:


DF = {} #key:language
WriteDir=HOME+'/data/SrcRefHypRawDA'
for lang in ['cs-en', 'de-en', 'fi-en', 'ru-en']:
    DF[lang] = combineData(lang)
    saveDf2Csv(WriteDir+'/newstest2015-2017.'+lang+'.csv', DF[lang])

