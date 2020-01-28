# Project name here
> Summary description here.


This file will become your README and also the index of your documentation.

## Install

`pip install your_project_name`

## How to use

Fill me in please! Don't forget code examples:

```python
from fast_neptune.core import *
```

```python
# Neptune login
from neptune.sessions import Session
import getpass

api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)
user_name = "danywin"
project_name = "fast-neptune"
project = session.get_project(project_qualified_name=f'{user_name}/{project_name}')
```

```python
#code
from fastai.vision import *

path = untar_data(URLs.MNIST_SAMPLE)
data = ImageDataBunch.from_folder(path)
learn = cnn_learner(data, models.resnet18, metrics=accuracy)
```

    A new version of the dataset is available.
    Downloading http://files.fast.ai/data/examples/mnist_sample
    



<div>
    <style>
        /* Turns off some styling */
        progress {
            /* gets rid of default border in Firefox and Opera. */
            border: none;
            /* Needs to be in here for Safari polyfill so background images work as expected. */
            background-size: auto;
        }
        .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
            background: #F44336;
        }
    </style>
  <progress value='3145728' class='' max='3214948', style='width:300px; height:20px; vertical-align: middle;'></progress>
  97.85% [3145728/3214948 00:05<00:00]
</div>



    
     Download of http://files.fast.ai/data/examples/mnist_sample.tgz has failed after 5 retries
     Fix the download manually:
    $ mkdir -p C:\Users\Daniel\.fastai\data
    $ cd C:\Users\Daniel\.fastai\data
    $ wget -c http://files.fast.ai/data/examples/mnist_sample.tgz
    $ tar -zxvf mnist_sample.tgz
    
    And re-run your code once the download is successful
    
    


    An exception has occurred, use %tb to see the full traceback.
    

    SystemExit: 1
    


```python
nb_name = "index.ipynb"
globs = globals()

with fast_experiment(project,nb_name,globs) as exp:
    pass
```

    https://ui.neptune.ai/danywin/EnsembleDropout/e/EN-171

