# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:13:34 2020

@author: Robert Schuldt

Attempting to Fuzzy math the names of nursing homes using the data I collected
from the NPI database so that we can link them to the CCN numbers that we have 
in another file. WIll be using the Levenstein package to attempt this
"""
#Initial packages I will need to create the api request and dump into json
import datetime
import requests
import pandas as pd

from fuzzywuzzy import fuzz, process

ts = datetime.datetime.now().isoformat()

print(ts)

ccn_file = "*******************************************.csv"
df_ccn = pd.read_csv(ccn_file, header = 0)
#Want to give my column a legible name 

df_ccn = df_ccn[['PRVDR_CCN', 'PRVDR_NAME']]

#Now bring in my other file with the NPI numbers and names 
org_fle = r'C:\Users\3043340\Box\Dr. Felix Work\NPI Crosswalk\npi_org_names.csv'
df_npi = pd.read_csv(org_fle, header = 0)

def match_term(term, list_names, min_score =0 ):
    max_score = -1
    max_name = ""
    for term2 in list_names:
        score = fuzz.ratio(term, term2)
        if (score> min_score) & (score > max_score):
            max_name = term2
            max_score = score
    return(max_name, max_score)


    
dict_list = []

for name in df_npi['Organization Name']:
    match= match_term(name, df_ccn['PRVDR_NAME'], 70)
    dict_ = {}
    dict_.update({'NPI NAME':name})
    dict_.update({"Match Name": match[0]})
    dict_.update({"score": match[1]})
    dict_list.append(dict_)
    
df = pd.DataFrame(dict_list)

#This program works, but there are too many similarities in the names
#The program functions, but will not work for the matching problem 

df.to_csv(r'******************************\fuzzy_matching.csv')