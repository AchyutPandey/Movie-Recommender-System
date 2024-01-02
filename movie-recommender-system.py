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

movies.head()


# In[22]:


def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        #this converts the above int o list of dict rather than in string
        if i['job']=='Director':
            l.append(i['name'])
            break
    return l


# In[23]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[24]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[25]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])


# In[26]:


movies.head()


# In[27]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['crew']


# In[28]:


movies.head()

# In[29]:


new_df=movies[['movie_id','title','tags']]
new_df


# In[30]:


new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))


# In[31]:


new_df.head()


# In[32]:


new_df['tags']=new_df['tags'].apply(lambda x:x.lower())


# In[33]:


new_df


# In[34]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
#replaces similar words by common word


# In[35]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[36]:


new_df['tags'] = new_df['tags'].apply(stem)


# In[37]:


vectors=cv.fit_transform(new_df['tags']).toarray()


# In[38]:


cv.get_feature_names_out()


# In[39]:


from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)


# In[40]:


similarity[2]


# In[41]:


def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)
    return


# In[52]:


input_movie=input("Enter movie name: ")
try:
    recommend(input_movie)
except:
    print("Movie not found in database :( ")



