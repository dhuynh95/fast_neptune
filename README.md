# fast-neptune
> Quickly track your Jupyter Notebook experiments with NeptuneML


`fast-neptune` is a library that helps you quickly record all the information you need to launch your experiments, when you are using Jupyter Notebooks. Reproducibility has become a crucial issue in Machine Learning, not only for research, but also for real world applications, where we want to have robust results, and track every set of parameters tested, along with their results.

`fast-neptune` spirit is highly inspired from [nbdev](http://nbdev.fast.ai/) in the user experience, so it is recommended to have a look first at it.

Furthermore, `fast-neptune` is built upon the solution [neptune-ml](https://neptune.ai/) which allows users to quickly record on a public or private repository. Following the [quick introduction](https://docs.neptune.ai/python-api/introduction.html) is a plus to understand `fast-neptune`, but as we will see it's quite intuitive.

## Install

`fast-neptune` is available on pypi so you can simply run :

`pip install fast-neptune`

## How to use

`fast-neptune` has implemend several features to help you when you run ML experiments.
These include :
<ul>
    <li>metadata about the machine where the code is run, including OS, and OS version</li>
    <li>requirements of the notebook where the experiments are run</li>
    <li>parameters used during the experience, which means the names of the values of the variables you want to track</li>
    <li>code you used during the run that you want to record</li>
</ul>

Note that code and parameters are not mandatorily tracked, while the two former are, though the whole purpose of this library is to facilitate the tracking of parameters and code.

### Metadata 

Metadata is tracked about the requirements used and information about the Python version and OS used.

They are added automatically when an experiment is created, through the functions [`get_metadata`](/core#get_metadata) and [`create_requirements`](/core#create_requirements).

### Property

Properties refer to variables you want to record. 

To record properties, simply add `#property` to each cell containing the variables you want to record.

Note : if one variable in a property is a file encapsulated in a `Path` object, it is automatically tracked, and this file will be sent to NeptuneML. You can disable this option when creating the experiment.

### Code

Code cells can also be tracked.

To do so, simply add `#code` to each cell you want to record. You have the possibility to specify under what name the cell code will be registered. By default, all cells with `#code` will be added chronogically to the file "main.py", but if you can put them in specific files by adding the name of the module you want them to be put in.

Example : add `#code dataloading.py` to the cells that take care of the data loading.

## Example with fastai vision to train a MNIST classifier

To understand more how all of this fit in, we will follow a simple example, using fastai library.

First we will log in using NeptuneML

```python
# Neptune login
from neptune.sessions import Session
import getpass

# First we get the token
api_token = getpass.getpass("Please enter your NeptuneML API token : ")
session = Session(api_token=api_token)

# Then we enter user name and project
user_name = "danywin"
project_name = "fast-neptune"

project = session.get_project(project_qualified_name=f'{user_name}/{project_name}')
```

    Please enter your NeptuneML API token : 
    

    WARNING: Instantiating Session without specifying a backend is deprecated and will be removed in future versions. For current behaviour use `neptune.init(...)` or `Session.with_default_backend(...)
    WARNING: It is not secure to place API token in your source code. You should treat it as a password to your account. It is strongly recommended to use NEPTUNE_API_TOKEN environment variable instead. Remember not to upload source file with API token to any public repository.
    

Now we will start using `fast-neptune`.

First we will record the code used to load the data and learner. To do so, we simply add `#code` to the cell used to load the data.

```python
from fast_neptune.core import *
```

```python
#code dataloading.py
from fastai.vision import *

path = untar_data(URLs.MNIST_SAMPLE)
data = ImageDataBunch.from_folder(path)
learn = cnn_learner(data, models.resnet18, metrics=accuracy)
```

Then we want to keep track of the number of epochs during training, and the learning rate we used. To do so we add `#property` to the cell we want to track.

```python
#property
n_epoch = 1
lr = 1e-2
```

Finally we use [`fast_experiment`](/core#fast_experiment) to create our experiment. Note that you must pass it the name of the notebook you are using for your experiments, and the global variables you are currently using to record each variable in the properties cells.

Here we will create an experiment, then record the validation accuracy.

```python
#code
nb_name = "index.ipynb"
globs = globals()

with fast_experiment(project,nb_name,globs) as exp:
    learn.fit_one_cycle(n_epoch,lr)
    pred,y = learn.get_preds()
    
    score = accuracy(pred,y).item()
    exp.send_metric("valid_accuracy",score)
```

    https://ui.neptune.ai/danywin/fast-neptune/e/FAS1-18
    


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>epoch</th>
      <th>train_loss</th>
      <th>valid_loss</th>
      <th>accuracy</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0.052504</td>
      <td>0.014153</td>
      <td>0.994603</td>
      <td>00:04</td>
    </tr>
  </tbody>
</table>






Now if we go on the link provided by NeptuneML we can have a closer look at this experiment :

Here we can see the parameters that were registered, including epoch, learning rate, OS, and Python version.

![Parameters](imgs\parameters.PNG)

In the source code tab, we can have a look at the bits of code we registered, here the dataloading.
![Code](imgs\code.PNG)

In the artifacts we also have the modules used in this notebook with their version : 

![Requirements](imgs\requirements.PNG)

Finally, we logged the validation accuracy, which can be found in the Logs tab : 

![Parameters](imgs\valid_score.PNG)
