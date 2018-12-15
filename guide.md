
# Project setup

This is a notebook that details the steps that I take to create a data science project complete with environments, packages, folder structrue and git. It exists to remind myself what I do to set things up and also may help other people to follow and tweak this as they see fit.

This uses
- cookiecutter datascience for folder structure
- pipenv for package and environment management

To get the new environment working, it is assumed you have jupyter notebook already installed on your user within linux and gets jupyter notebook using the pipenv environment you create.

I had some issues with pipenv giving "TypeError: 'module' object is not callable", however setting pipenv to use pip 18.0 appears to work. I used this command to do this as suggested here: https://github.com/pypa/pipenv/issues/2871. There are a few other suggestions if this does not work.


```bash
%%bash
pipenv run pip install pip==18.0
```

## Folder structure

It is worth noting before we go any further that none of this is binding. Adapt this to suit you and your project (conservatively), this is here give you something that works for a general project to save you time, not tell you how to work.

We can use a standard folder structure so that it is easy to understand where everything is. For this we use cookiecutter.

Why would we want to use this for our projects? Well it gives a number of advantages...

- It gives us a workable structure in one go and saves time meaning we can get on with doing actual work
- It encourages good practice and a sensible workflow with modular code, explorations and outputs
- Well organised code and file structure helps the project document itself saving you time and gives and helps people get up to speed with your work, including future you!

You can have a look a documentation discussing this structure here:http://drivendata.github.io/cookiecutter-data-science/#cookiecutter-data-science but there are some important principles that this follows below.

### Data is immutable
This allows your work to be replicated if someone has the original data and the code that processes the data

### Notebooks are for hacky exploration and outputs
They are not that great for the heavy lifting of processing your data science projects. For that use .py files as you can import these into multiple notebooks for reuse and document them as well as use tools like pyflake and unittest to check your code and make sure it is of high quality.

### Analysis is linear and deterministic
What this means is there are a number of steps to follow in a set order to get your outputs build from the environment.  If your code is adequately documented and well organised, then anyone else should be able to follow these steps to run your analysis and replicate your results.

### Always use a virtual environment 
This is to avoid the "it used to work" or "it works on my machine" problems. Basically if you want to share your code or use it again in future, use an environment. I use pipenv as it wraps up pip and virtualenv into one package which I think makes things easy and simple to use. This should ensure you are using the same package versions in your code.

### Change the layout conservatively
Do you really need to change the structure? really really? Remember any change makes your project more opaque and less understandable as it is a devates from what people might expect by reading the cookiecutter documentation here.

## Step one - download and set up cookiecutter datasciene project

Before you start, go to your projects folder with the terminal using the 'cd' command

We install cookiecutter if we haven't got it on our user. We do this with pip as we don't want it to create a new environment. Cookiecutter will ask you questions like the name of your project and the like. Fill in as neccesary.

It will then create a folder for you with its structure.


```bash
%%bash

pip install cookiecutter
cookiecutter https://github.com/drivendata/cookiecutter-data-science
```

## Step two - clone this repo
Navigate into this folder that you've created with cd <folder name> if you can't remember use ls to view the folders.

Clone this repo into your new folder where you are going to work on this project


```bash
%%bash

git init 
git remote add origin PATH/TO/REPO 
git fetch 
git checkout -t origin/master
```

## Step three - Set. up. everything.

Enter the created folder and run this bash script to install cookiecutter datascience and a bunch of useful data science python modules, kind of slimlar to anaconda install, so you're ready to go. Since you are useing pipenv, this will set up an environment for you with these packages as well as the cookiecutter folder structure.

This bit should take a while, so make a coffee or something!

If you want you can edit the bootstrap.sh file with a text editor to cut down the packages required.


```bash
%%bash
bash bootstrap.sh
```

## Step four - get the name of your pipenv environment

First we need to pipenv install ipykernel in the environment. But, our bash script has already done that so we can skip that step and just get then name of the environment. If we go to the folder in the terminal and run the  command `pipenv shell`in the command line we see that it says something like <env-name> user@machine:~/path/to/folder we need the <env-name> for the next bit so exit out of the environment and type in the following command to add the environment to jupyter. For this to work, you need to replace <env-name> with the environment name.


```bash
%%bash
pipenv shell
python -m ipykernel install --user --name=<env-name>
```

## Step five
Remove the origin for the datascience bootstrap code.


```python
git remote rm origin
```

## Step six - create a new repo and push

Create a new repo in git then commit


```bash
%%bash
git init
git add .
git commit -m
git push -u origin master
```
