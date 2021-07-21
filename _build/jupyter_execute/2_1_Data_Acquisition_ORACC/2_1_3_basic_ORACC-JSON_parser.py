#!/usr/bin/env python
# coding: utf-8

# # Extract Lemmatization from ORACC JSON: Basic Parser
# The code in this notebook will parse [ORACC](http://oracc.org) `JSON` files to extract lemmatization data for one or more projects. The resulting `csv` (Comma Separated Values) file is named `parsed.csv` and has two fields: a Text ID (e.g. `dcclt/Q000039`) and a string of lemmas in the format `lugal[king]N` (or `šarru[king]N` for Akkadian texts).
# 
# The output of the Basic Parser contains *only* text IDs and lemmas. This format is useful for so-called [bag of words](https://en.wikipedia.org/wiki/Bag-of-words_model) techniques such as word clouds or [topic modeling](https://en.wikipedia.org/wiki/Topic_model). The `JSON` files, however, contain a wealth of other data, including language (Sumerian, Akkadian, Emesal, etc.), orthographic form, morphology (currently only for Sumerian and Emesal), line numbers, breakage, etc. The extended JSON parser notebook, building upon the techniques demonstrated here, will show how to extract any type of data.

# In[ ]:


import pandas as pd
import zipfile
import json
from tqdm.auto import tqdm
import os
import sys
util_dir = os.path.abspath('../utils')
sys.path.append(util_dir)
import utils


# ## 0 Create Directories, if Necessary
# The two directories needed for this script are `jsonzip` and `output`. The directories are created with the function `make_dirs()` from the `utils` module. 

# In[ ]:


os.makedirs('jsonzip', exist_ok = True)
os.makedirs('output', exist_ok = True)


# ## 1.1 Input Project Names
# Provide a list of one or more project names, separated by commas. Note that subprojects must be listed separately, they are not included in the main project. For instance:
# 
# `saao/saa01,saao/saa02,blms`
# 
# The input is split into a proper list that python can iterate over using the `format_project_list()` function in the `utils` module. The code of this function is discussed in more detail in 2.1.0. Download ORACC JSON Files.

# In[ ]:


projects = input('Project(s): ').lower()
project_list = utils.format_project_list(projects)


# ## 1.2 Download the ZIP files.
# Download the zipped JSON files using the `oracc_download()` function in the `utils` module. The code of this function is discussed in more detail in 2.1.0. Download ORACC JSON Files.

# In[ ]:


project_list = utils.oracc_download(project_list)


# ## <a name="head21"></a>2.1 The `parsejson()` function
# The `parsejson()` function will "dig into" the `json` file (transformed into a dictionary) until it finds the relevant data. The `json` file consists of a hierarchy of `cdl` nodes; only the lowest nodes contain lemmatization data. The function goes down this hierarchy by calling itself when another `cdl` node is encountered. For more information about the data hierarchy in the [ORACC](http://oracc.org) `json` files, see [ORACC Open Data](http://oracc.org/doc/opendata/index.html).
# 
# The first argument of the `parsejson()` function is a `JSON` object, essentially a Python dictionary that initially contains the entire contents of the original JSON file. The code takes the key `cdl` the value of which is a list of `JSON` dictionaries. Iterating through these dictionaries, if a dictionary contains another `cdl` node, the function calls itself with this lower-level dictionary as argument. This way the function digs deeper and deeper into the `JSON` tree, until it does not encounter a `cdl` key anymore. Here we are at the level of individual words. The code checks for a key `f`, if it exists the value of that key (another dictionary) is appended to the list `l`. The list `l` will become a list of dictionaries, where each dictionary represents a single word and the list represents the vocabulary of a single text with the words in their original order.
# 
# The second argument of the function, `id_text`, consists of a project abbreviation, such as `blms` or `cams/gkab` plus a text ID, in the format `cams/gkab/P338616` or `dcclt/Q000039`. This ID is added to the lemmatization data of every word.

# In[ ]:


def parsejson(text, id_text):
    lemmas = []
    for JSONobject in text["cdl"]:
        if "cdl" in JSONobject: 
            lemmas.extend(parsejson(JSONobject, id_text))
        if "f" in JSONobject:
            lemm = JSONobject["f"]
            lemm["id_text"] = id_text
            lemmas.append(lemm)
    return lemmas


# ## 2.2 Call the `parsejson()` function for every `JSON` file
# The code in this cell will iterate through the list of projects entered above (1.1). For each project the `JSON` zip file is located in the directory `jsonzip`, named PROJECT.zip. The `zip` file contains a directory that is called `corpusjson` that contains a JSON file for every text that is available in that corpus. The files are called after their text IDs in the pattern `P######.json` (or `Q######.json` or `X######.json`).
# 
# The function `namelist()` of the `zipfile` package is used to create a list of the names of all the files in the ZIP. From this list we select all the file names in the `corpusjson` directory with extension `.json` (this way we exclude the name of the directory itself). 
# 
# Each of these files is read from the `zip` file and loaded with the command `json.loads()`, which transforms the string into a proper JSON object. 
# 
# This JSON object (essentially a Python dictionary), which is called `data_json` is now sent to the `parsejson()` function. The function returns a list of lemmata (each lemma represented by a dictionary). The `extend()` method is used to add this list to the list `lemm_l`, one document at the time. In the end, `lemm_l` will contain as many list elements as there are words in all the texts in the projects requested.

# In[ ]:


lemm_l = [] # initiate the list that will hold all the lemmatization data of all texts in all requested projects
for project in project_list:
    file = f"jsonzip/{project.replace('/', '-')}.zip"
    try:
        zip_file = zipfile.ZipFile(file)       # create a Zipfile object
    except:
        errors = sys.exc_info() # get error information
        print(file), print(errors[0]), print(errors[1]) # and print it
        continue
    files = zip_file.namelist()     # list of all the files in the ZIP
    files = [name for name in files if "corpusjson" in name and name[-5:] == '.json']                                                                                                  #that holds all the P, Q, and X numbers.
    for filename in tqdm(files, desc=project):                            #iterate over the file names
        id_text = project + filename[-13:-5] # id_text is, for instance, blms/P414332
        try:
            text = zip_file.read(filename).decode('utf-8')         #read and decode the json file of one particular text
            data_json = json.loads(text)                # make it into a json object (essentially a dictionary)
            lemm_l.extend(parsejson(data_json, id_text))               # and send to the parsejson() function
        except:
            errors = sys.exc_info() # get error information
            print(filename), print(errors[0]), print(errors[1]) # and print it
    zip_file.close()


# ## 3 Data Structuring
# ### 3.1 Transform the Data into a DataFrame
# The list `lemm_l` is transformed into a `pandas` dataframe (`word_df`) for further manipulation. The `pandas` function `fillna('')` fills gaps in the dataframe. If a particular data field is not available for a particular row, `pandas` will fill that cell with NaN ("Not a Number"). The data type of NaN is numeric, which creates problems in string manipulation further down the road (for instance in creating a Lemma column, section 3.2). The function `fillna()` will fill all empty cells with the argument it is given - in this case the empty string.
# 
# For various reasons not all JSON files will have all data types that potentially exist in an [ORACC](http://oracc.org) lemmatization. For instance, only Sumerian words have a `base`, so if your data set has no Sumerian, this column will not exist in the DataFrame. Where such fields are referenced below, the code may fail and you may need to adjust some lines.

# In[ ]:


word_df = pd.DataFrame(lemm_l)
word_df = word_df.fillna('')      # replace NaN (Not a Number) with empty string
word_df


# ## 3.1 Remove Spaces and Commas from Guide Word and Sense
# Spaces and commas in Guide Word and Sense may cause trouble in computational methods in tokenization, or when saved in Comma Separated Values format. All spaces and commas are replaced by hyphens and nothing (empty string), respectively. By default the `replace()` function in `pandas` will match the entire string (that is, "lugal" matches "lugal" but there is no match between "l" and "lugal"). In order to match partial strings the parameter `regex` must be set to `True`.
# 
# The `replace()` function takes a nested dictionary as argument. The top-level keys identify the columns on which the `replace()` function should operate (in this case 'gw' and 'sense'). The value of each key is another dictionary with the search string as key and the replace string as value.

# In[ ]:


findreplace = {' ' : '-', ',' : ''}
word_df = word_df.replace({'gw' : findreplace, 'sense' : findreplace}, regex = True)


# ## 3.2 Create a `lemma` column
# A lemma, [ORACC](http://oracc.org) style, combines Citation Form, GuideWord and POS into a unique reference to one particular lemma in a standard dictionary, as in `lugal[king]N` (Sumerian) or `šarru[king]N` (Akkadian). Usually, not all words in a text are lemmatized, because a word may be (partly) broken and/or unknown. Unlemmatized and unlemmatizable words will receive a place-holder lemmatization that consists of the transliteration of the word (instead of the Citation Form), with `NA` as GuideWord and `NA` as POS, as in `i-bu-x[NA]NA`. Note that `NA` is a string. 

# In[ ]:


word_df["lemma"] = word_df["cf"] + '[' + word_df["gw"] + ']' + word_df["pos"]
word_df.loc[word_df["cf"] == "" , 'lemma'] = word_df['form'] + '[NA]NA'
word_df[['id_text', 'lemma']]


# ## 3.3 Group by Textid
# Get all the lemmas that belong to a single text in one row (one row = one document). The `agg()` (aggregate) function, which works on the result of a `groupby()` process aggregates columns of the original dataframe. The aggregate function takes a dictionary in which the keys are column names and the values are functions to be used in the aggregation process. The example below has only one such function (`' '.join` will join all entries in the colum `lemma` with a space in between); one may specify (the same or different) functions for different columns, for instance:
# ```python
# word_df = word_df.groupby("textid").agg({"lemma": ' '.join, "base": ' '.join})
# ```
# The process will create a compound index. It is useful to flatten the index with a reset (`reset_index()`).

# In[ ]:


doc_df = word_df.groupby("id_text").agg({"lemma": ' '.join})
doc_df = doc_df.reset_index()
doc_df


# # 4 Save the Results
# ## 4.1 Save Results in CSV file
# The output file is called `parsed.csv` and is placed in the directory `output`. In most cases, `csv` files open automatically in Excel. This program does not deal well with `utf-8` encoding. If you intend to use the file in Excel, change `encoding ='utf-8'` to `encoding='utf-16'`. For usage in computational text analysis applications `utf-8` is usually preferred. The option `index=False` excludes the (numerical) index from the saved `csv`.

# In[ ]:


savefile =  'parsed.csv'
with open(f'output/{savefile}', 'w', encoding="utf-8") as w:
    doc_df.to_csv(w, index=False)


# ## 4.2 Pickle
# The Pandas function `to_pickle()` writes a binary file that can be opened in a later phase of the project with the `read_pickle()` command and will reproduce exactly the same DataFrame. The resulting file cannot be used in other programs but preserves the data structure of the DataFrame.

# In[ ]:


pickled = "output/parsed.p"
doc_df.to_pickle(pickled)


# In[ ]:




