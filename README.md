# Project name here
> Summary description here.


This file will become your README and also the index of your documentation.

## Install

`pip install your_project_name`

## How to use

Fill me in please! Don't forget code examples:

```python
# Neptune login
from neptune.sessions import Session
import getpass

api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)
project = session.get_project(project_qualified_name='danywin/fast-neptune')
```

    Please enter your NeptuneML API token :
    

    WARNING: Instantiating Session without specifying a backend is deprecated and will be removed in future versions. For current behaviour use `neptune.init(...)` or `Session.with_default_backend(...)
    WARNING: It is not secure to place API token in your source code. You should treat it as a password to your account. It is strongly recommended to use NEPTUNE_API_TOKEN environment variable instead. Remember not to upload source file with API token to any public repository.
    

```python
name = "MNIST-example"
description = "Demonstration of fast_neptune on MNIST using fastai"
```
