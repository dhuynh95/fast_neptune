#!/usr/bin/env python
# coding: utf-8

# # Project name here
# 
# > Summary description here.

# This file will become your README and also the index of your documentation.

# ## Install

# `pip install your_project_name`

# ## How to use

# Fill me in please! Don't forget code examples:

# In[6]:


from fast_neptune.core import *


# In[7]:


#code
print("Coucou")


# In[8]:


nb_name = "index.ipynb"
get_codes(nb_name)


# In[9]:


# Neptune login
from neptune.sessions import Session
import getpass

api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)
project = session.get_project(project_qualified_name='danywin/EnsembleDropout')


# In[13]:


nb_name = "index.ipynb"
globs = globals()
with fast_experiment(project,nb_name,globs) as exp:
    pass


# In[ ]:




