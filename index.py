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

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


from fast_neptune.core import *


# In[3]:


# Neptune login
from neptune.sessions import Session
import getpass

api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)
user_name = "danywin"
project_name = "fast-neptune"
project = session.get_project(project_qualified_name=f'{user_name}/{project_name}')


# In[4]:


#code
from fastai.vision import *

path = untar_data(URLs.MNIST_SAMPLE)
data = ImageDataBunch.from_folder(path)
learn = cnn_learner(data, models.resnet18, metrics=accuracy)


# In[5]:


#property
n_epoch = 1
lr = 1e-2


# In[6]:


nb_name = "index.ipynb"
globs = globals()

with fast_experiment(project,nb_name,globs) as exp:
    learn.fit_one_cycle(n_epoch,lr)
    pred,y = learn.get_preds()
    
    score = accuracy(pred,y).item()
    exp.send_metric("valid_accuracy",score)


# In[15]:


get_properties_from_cells(nb_name,globs)


# In[16]:


get_codes(nb_name)


# In[8]:


get_ipython().run_line_magic('pinfo2', 'fast_experiment')

