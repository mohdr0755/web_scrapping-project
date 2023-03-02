#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
import nltk
import requests
import bs4 as bfs
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from textblob import TextBlob
import csv


# In[25]:


df = pd.read_excel('D:\Demo\DataScience\#PROJECTS\BlackcofferTextAnalysis/in.xlsx',index_col=0)
df


# In[26]:


li = [url for url in df['URL']]
li


# In[27]:


articles = []
for url in li:
    articles.append(bfs.BeautifulSoup(requests.get(url,headers={"User-Agent": "XY"}).content,'html.parser').find(attrs= {"class":"td-post-content"}).text)


# In[28]:


len(articles)


# In[29]:


stop_words = list(set(stopwords.words('english')))


# In[30]:


sentences = []
for article in articles:
  sentences.append(len(sent_tokenize(article)))


# In[33]:


len(sentences)


# In[36]:


cleaned_articles = [' ']*len(articles)


# In[39]:


for i in range(len(articles)):
  for w in stop_words:
    cleaned_articles[i]= articles[i].replace(' '+w+' ',' ').replace('?','').replace('.','').replace(',','').replace('!','')


# In[42]:


words = []
for article in articles:
  words.append(len(word_tokenize(article)))


# In[43]:


words_cleaned = []
for article in cleaned_articles:
  words_cleaned.append(len(word_tokenize(article)))


# In[44]:


dictionary = pd.read_excel('D:\Demo\DataScience\#PROJECTS\BlackcofferTextAnalysis/LoughranMcDonald_MasterDictionary_2020.xlsx')


# In[45]:


dictionary.head()


# In[46]:


positive_words = list(dictionary[dictionary['Positive']==2009]['Word'])
positive_words = [word.lower() for word in positive_words]


# In[47]:


negative_words = list(dictionary[dictionary['Negative']==2009]['Word'])


# In[48]:


positive_score = [0]*len(articles)
for i in range(len(articles)):
  for word in positive_words:
    for letter in cleaned_articles[i].lower().split(' '):
      if letter==word:
        positive_score[i]+=1


# In[49]:


negative_score = [0]*len(articles)
for i in range(len(articles)):
  for word in negative_words:
    for letter in cleaned_articles[i].upper().split(' '):
      if letter==word:
        negative_score[i]+=1


# In[50]:


words_cleaned = np.array(words_cleaned)
sentences = np.array(sentences)


# In[51]:


df['POSITIVE SCORE'] = positive_score
df['NEGATIVE SCORE'] = negative_score


# In[52]:


df['POLARITY SCORE'] = (df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/ ((df['POSITIVE SCORE'] +df['NEGATIVE SCORE']) + 0.000001)


# In[53]:


df['SUBJECTIVITY SCORE'] = (df['POSITIVE SCORE'] + df['NEGATIVE SCORE'])/( (words_cleaned) + 0.000001)


# In[54]:


df['AVG SENTENCE LENGTH'] = np.array(words)/np.array(sentences)


# In[55]:


complex_words = []
sylabble_counts = []


# In[56]:


for article in articles:
  sylabble_count=0
  d=article.split()
  ans=0
  for word in d:
    count=0
    for i in range(len(word)):
      if(word[i]=='a' or word[i]=='e' or word[i] =='i' or word[i] == 'o' or word[i] == 'u'):
           count+=1
#            print(words[i])
      if(i==len(word)-2 and (word[i]=='e' and word[i+1]=='d')):
        count-=1;
      if(i==len(word)-2 and (word[i]=='e' and word[i]=='s')):
        count-=1;
    sylabble_count+=count    
    if(count>2):
        ans+=1
  sylabble_counts.append(sylabble_count)
  complex_words.append(ans) 


# In[57]:


df['PERCENTAGE OF COMPLEX WORDS'] = np.array(complex_words)/np.array(words)


# In[58]:


df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])


# In[59]:


df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']


# In[60]:


df['COMPLEX WORD COUNT'] = complex_words


# In[61]:


df['WORD COUNT'] = words


# In[62]:


df['SYLLABLE PER WORD'] = np.array(sylabble_counts)/np.array(words)


# In[63]:


total_characters = []
for article in articles:
  characters = 0
  for word in article.split():
    characters+=len(word)
  total_characters.append(characters) 


# In[64]:


personal_nouns = []
personal_noun =['I', 'we','my', 'ours','and' 'us','My','We','Ours','Us','And'] 
for article in articles:
  ans=0
  for word in article:
    if word in personal_noun:
      ans+=1
  personal_nouns.append(ans)


# In[65]:


df['PERSONAL PRONOUN'] = personal_nouns
#as the all pronouns were cleared when clearing the stop words.


# In[66]:


df['AVG WORD LENGTH'] = np.array(total_characters)/np.array(words)


# In[67]:


df


# In[69]:


import os
os.chdir("D:\Demo\DataScience\#PROJECTS\BlackcofferTextAnalysis")


# In[70]:


os.getcwd()


# In[71]:


df.to_excel("Output Data Structure.xlsx")


# In[ ]:




