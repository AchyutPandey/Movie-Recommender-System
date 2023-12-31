#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


credits=pd.read_csv('tmdb_5000_credits.csv')
movies=pd.read_csv('tmdb_5000_movies.csv')


# In[3]:


movies.head()


# In[4]:


credits.head()


# In[5]:


credits.head(1)['crew'].values


# In[6]:


movies = movies.merge(credits,on='title')


# In[7]:


movies.head()


# In[8]:


movies.info()


# In[9]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[10]:


movies.isnull().sum()


# In[11]:


movies=movies.dropna()


# In[12]:


movies.isnull().sum()


# In[13]:


movies.iloc[0].genres


# In[14]:


import ast


# In[15]:


def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        #this converts the above int o list of dict rather than in string
        l.append(i['name'])
    return l


# In[16]:


movies['genres']=movies['genres'].apply(convert)


# In[17]:


movies['keywords']=movies['keywords'].apply(convert)


# In[18]:


movies.head()


# In[19]:


def convert3(obj):
    l=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            l.append(i['name'])
            counter+=1
        else:
            break
    return l


# In[20]:


movies['cast'] = movies['cast'].apply(convert3)


# In[21]:




