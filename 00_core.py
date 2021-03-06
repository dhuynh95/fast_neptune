#!/usr/bin/env python
# coding: utf-8

# In[1]:


#hide
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


# default_exp core


# In[3]:


#export
from nbdev.export import check_re,read_nb
from pathlib import Path
import re
import os
import platform


# # module name here
# 
# > API details.

# ## Code cells

# In[4]:


#export
_re_blank_code = re.compile(r"""
# Matches any line with #export or #exports without any module name:
^         # beginning of line (since re.MULTILINE is passed)
\s*       # any number of whitespace
\#\s*     # # then any number of whitespace
code  # export or exports
\s*       # any number of whitespace
$         # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)

_re_mod_code = re.compile(r"""
# Matches any line with #export or #exports with a module name and catches it in group 1:
^         # beginning of line (since re.MULTILINE is passed)
\s*       # any number of whitespace
\#\s*     # # then any number of whitespace
code  # export or exports
\s*       # any number of whitespace
(\S+)     # catch a group with any non-whitespace chars
\s*       # any number of whitespace
$         # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)


# In[5]:


#export
def is_code(cell, default="main.py"):
    "Check if `cell` is to be exported and returns the name of the module to export it if provided"
    if check_re(cell, _re_blank_code):
        return default
    tst = check_re(cell, _re_mod_code)
    return os.path.sep.join(tst.groups()[0].split('.')).replace("\\",".") if tst else None


# In[6]:


#export
from collections import defaultdict

def get_codes(fn:str,default:str = "main.py") -> dict:
    nb = read_nb(fn)
    
    module_to_code = defaultdict(str)
    
    module_to_code[default] = ""
    
    for cell in nb["cells"]:
        code = is_code(cell,default)
        if code:
            module_to_code[code] += cell["source"]
    
    return dict(module_to_code)


# ## Properties

# ### OS information

# In[7]:


#export
def get_metadata() -> dict:
    data = {
        "os":os.name,
        "system":platform.system(),
        "release":platform.release(),
        "python_version":platform.python_version()
    }
    return data


# In[8]:


get_metadata()


# ### Modules information

# In[2]:


get_ipython().system('echo coucou')


# In[3]:


from pipreqs.pipreqs import init


# In[5]:


from docopt import docopt


# In[7]:


subprocess.check_output(["pipreqs","./","--force"])


# In[9]:


#export
def create_requirements(fn):
    # Convert the notebook to a python file
    os.system(f"jupyter nbconvert --to=python {fn}")
    
    # Create the requirements file
    os.system("pipreqs ./ --force")


# ### Properties cells

# In[10]:


#export
_re_blank_property = re.compile(r"""
# Matches any line with #export or #exports without any module name:
^         # beginning of line (since re.MULTILINE is passed)
\s*       # any number of whitespace
\#\s*     # # then any number of whitespace
property  # export or exports
\s*       # any number of whitespace
$         # end of line (since re.MULTILINE is passed)
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)

_re_obj_def = re.compile(r"""
# Catches any 0-indented object definition (bla = thing) with its name in group 1
^          # Beginning of a line (since re.MULTILINE is passed)
([^=\s]*)  # Catching group with any character except a whitespace or an equal sign
\s*=       # Any number of whitespace followed by an =
""", re.MULTILINE | re.VERBOSE)


# In[11]:


#export
def is_property(cell):
    "Check if `cell` is to be exported and returns the name of the module to export it if provided"
    if check_re(cell, _re_blank_property):
        return True
    else:
        return False

def add_cell_to_properties(cell: dict,properties: dict,globs:dict):
    """Adds all variables in the cell to the properties"""
    objs = _re_obj_def.findall(cell["source"])
    
    objs = {obj : globs[obj] for obj in objs}
    
    properties.update(objs)


# In[12]:


#export
def files_in_properties(properties:dict):
    """Returns the list of files from properties"""
    files = []
    for key,val in properties.items():
        if isinstance(val,Path) and val.is_file():
            files.append(str(val))
    return files


# In[13]:


#export
def get_properties_from_cells(fn: str,globs:dict,return_files:bool = True,):
    """Gets the properties from all #property cells"""
    
    nb = read_nb(fn)
    
    properties = {}
    
    for cell in nb["cells"]:
        if is_property(cell):
            add_cell_to_properties(cell,properties,globs=globs)

    files = files_in_properties(properties)
    return properties,files


# ## Wrapper

# In[41]:


#export
from contextlib import contextmanager
from neptune.projects import Project
from neptune.experiments import Experiment

@contextmanager
def fast_experiment(project: Project,nb_name:str,globs:dict,return_files: bool = True,
                    default:str = "main.py",**kwargs) -> Experiment:
    # First we get the code cells
    codes = get_codes(nb_name,default=default)
    
    # We write them in separate files
    for fn,code in codes.items():
        with open(fn,"w") as file:
            file.write(code)
            
    codes = list(codes.keys())
    
    # We get the properties
    properties,files = get_properties_from_cells(nb_name,globs=globs,return_files=return_files)
    metadata = get_metadata()
    properties.update(metadata)
    properties["nb_name"] = nb_name
    
    # We convert the dict keys to string
    for k,v in properties.items():
        properties[k] = str(v)
    
    exp = project.create_experiment(params=properties,upload_source_files=codes,**kwargs)
    
    # We create the requirements file and send it
    create_requirements(nb_name)
    exp.send_artifact("requirements.txt")
    
    for fn in files:
        exp.send_artifact(fn)
        
    yield exp
    
    exp.stop()
    
    # We remove the code files
    for fn in codes:
        os.remove(fn)
        
    os.remove("requirements.txt")


# In[8]:


#code
print("Coucou")


# In[9]:


nb_name = "00_core.ipynb"


# In[11]:


# Neptune login
from neptune.sessions import Session
from fast_neptune.core import fast_experiment
import getpass

api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)
project = session.get_project(project_qualified_name='danywin/fast-neptune')


# In[13]:


globs = globals()


# In[ ]:


with fast_experiment(project,nb_name,globs) as exp:
    pass

