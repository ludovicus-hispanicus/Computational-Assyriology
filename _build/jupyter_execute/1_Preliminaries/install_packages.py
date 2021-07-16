#!/usr/bin/env python
# coding: utf-8

# # Installing Anaconda
# 
# In order to install Anaconda go to http://anaconda.com and choose the DOWNLOAD tab. Make sure to download the version for Python 3.x. Installing Anaconda will also install Python 3, Jupyter Notebook, Jupyter Lab, numerous Python packages, and several other tools.
# 
# # Jupyter Lab 3.0
# 
# Jupyter Lab is an interface that opens in a web browser and that allows a user to see, edit, and run Jupyter Notebooks, Markdown documents, and other types of files. If you installed Python through Anaconda, you already have Jupyter Notebook and Jupyter Lab installed. If you have been working with Python, Jupyter Notebooks or Jupyter Lab for a while, please see below for potential compatability issues.
# 
# If your Jupyter Lab version is lower than 3.0, you will need to install `nodejs`, and `ipywidgets` as well as the ipywidgets extension of Jupyter lab. As of Jupyter 3.0 (Jan 2021) such installation is no longer necessary. There are various ways to check the Jupyter Lab version installed. If you installed with Anaconda you may simply open Anaconda Navigator and find the version number on the Jupyter Lab icon - or run the following command.

# In[ ]:


get_ipython().system('jupyter lab --version')


# If your Jupyter Lab version is higher than 3.0 you may skip the rest of this section. If not, you can update Jupyter Lab with the following command: 

# In[ ]:


get_ipython().run_line_magic('conda', 'update jupyterlab')


# Now check the version of Jupyter Lab with the command in the previous cell.

# # Jupyter Lab <3.0: Installing Jupyter Widgets; Enabling Jupyter Extensions

# If you need to keep the lower (<3.0) version of  Jupyter Lab, please follow the instructions below for installing `nodejs`, `ipywidgets`, and the Jupyter Lab ipywidgets extension. These are needed for creating progress bars, interactive visualizations, drop-down menus, etc.

# In[ ]:


get_ipython().run_line_magic('conda', 'install nodejs')
get_ipython().run_line_magic('conda', 'install ipywidgets')


# Finally, in order to make the widgets available in Jupyter Lab one needs to enable Jupyter Lab [extension manager](https://jupyterlab.readthedocs.io/en/stable/user/extensions.html) and install the widgets extension. The easiest way to do so is to run the cell below. Alternatively, open the Anaconda Prompt (Windows) or the Terminal (OS X) and copy this line, while omitting the initial exclamation mark.

# In[ ]:


get_ipython().system('jupyter labextension install @jupyter-widgets/jupyterlab-manager')


# You may need to close Jupyter Lab and open it again for the widgets extension to take effect. For more information about installing  and activating widgets see the overview [here](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-into-jupyterlab-1-or-2).

# # Some Trouble Shooting
# 
# If you just installed Anaconda and are new to working in Python or Jupyter, the above instructions should get you going. If you worked with Python, Jupyter Notebooks or Jupyter Lab before, you may need to update one or more of the components.
# 
# If the `%conda` lines above do not work, this means that you have an older version of IPython (the Python version that runs in Jupyter Notebooks). Commands that begin with the percentage sign belong to the IPython `magic` functions, expanding on the functionality of standard IPython. In this notebook we will use `%conda` to call the package manager (alternatively, you may use `%pip` with the same syntax for packages not available in conda, or if conda takes too much time). The %conda and %pip functions were introduced in IPython version 7.3. To check the IPython version on your machine, open the terminal (Mac OS X) or the Anaconda Prompt (Windows) and type 
# ```bash
# ipython --version
# ```
# If necessary, update Ipython with the following lines:

# In[ ]:


import sys
get_ipython().system('conda upgrade --yes --prefix {sys.prefix} ipython')


# Other  issues may arise if you have (older) versions of Jupyter Notebook, Jupyter Lab or Jupyter Widgets that are not compatible with each other. Check for compatability by following the instructions [here](https://pypi.org/project/jupyterlab/). Recommended are Jupyter Lab version 3.0 or higher; Jupyter Notebook version 6.0 or higher and Jupyter Widgets version 7.5 or higher. These recommendations, however, may quickly become obsolete as new functionality is developed. To check the versions on your machine you may run the following lines.

# In[ ]:


import ipywidgets
get_ipython().system('jupyter lab --version')
get_ipython().system('jupyter notebook --version')
ipywidgets.__version__


# If you need to update any of these, refer to the section below (Installing and Updating Python Packages).

# # Installing and Updating Python Packages
# With Anaconda, you already have a treasure trove of important Python packages, including `Pandas` (for data manipulation), `bokeh` (interactive visualisations), `requests` (for communicating with web sites), `scikit-learn` (machine learning), etc.
# 
# Inevitably, we will be using packages not included in the standard Anaconda distribution. Before they can be imported in a Python script such packages (or libraries) need to be installed. A package needs to be *imported* every time when a script is started. It needs to be *installed* only once (and updated subsequently, if necessary). An example of a package that will need to be installed is `pyldavis`, a visualization tool for topic modeling, which we will use in Chapter 5.
# 
# Installing packages can be a rather frustrating experience. The issue is that a computer may have more than one instance of Python installed (this is not unusual). In order to use Python packages within a Jupyter Notebook, they need to be associated with the so-called Python *kernel* that runs in the background of the notebook. For a more technical description of the issue and a solution see the [article](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/) by Jake VanderPlas in his [Pythonic Preambulations](https://jakevdp.github.io/) blog. 
# 
# Jake VanderPlas' solution has been implemented in two so-called IPython `magic` functions, namely `%conda` and `%pip`. In this notebook we will use the conda package manager.

# # Installation Code
# 
# The code for installing a package is
# ```python
# %conda install [package name]
# ```
# For upgrading a package to the latest version you may use
# ```python
# %conda upgrade [package name]
# ```
# With pip, upgrading is done as follows:
# ```python
# %pip install [package name] --upgrade
# ```
# 
# Examples:
# ```python
# %conda upgrade jupyterlab
# %conda install nodejs
# %conda install pyldavis
# %conda upgrade ipywidgets
# %pip install lexicalrichness --upgrade
# ```
# 
# Note that in some cases installing and upgrading may take a (very) long time and may result in the installation, removal, upgrading, or downgrading of a host of other packages. This is the case because conda will check for dependencies and for the compatibility of the newly installed software with other available packages. Under some circumstances conda may become entirely unusable. In such cases it may be advisable to install packages with pip.

# In[ ]:




