# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:46:45 2022

@author: rober
"""

import pandas as pd
df_temp = pd.DataFrame()

# %% get top source -----------------------------------------------------------

# returns the top source for a given author

def get_top_source(dataframe, author = 'default author'):
    top_source = dataframe['Publication'][dataframe['Author'].str.contains(author)].value_counts().reset_index().iloc[0,0]
    
    return top_source

# %% create list of top authors with sources ----------------------------------

# uses get_top_source to generate a list of top sources for given author list

def create_list_top_authors_w_sources(dataframe = df_temp, list_top_authors = 'default_list'):
    
    list_top_authors_sources = [get_top_source(dataframe, author) for author in list_top_authors[0:5]] 
    
    list_top_authors_w_sources = [list_top_authors[i] + ', ' + list_top_authors_sources[i] 
                                    for i in range(min(len(list_top_authors_sources),5))]
    
    return list_top_authors_w_sources

def create_list_top_authors_w_sources_others(dataframe = df_temp, list_top_authors = 'default_list'):
    
    list_top_authors_sources_others = [get_top_source(dataframe, author)
                if 
                len(dataframe['Publication'][dataframe['Author'].str.contains(author)].value_counts().reset_index()) == 1
                else get_top_source(dataframe, author) + ' and others'
                for author in list_top_authors[0:5]  # used in just one chart, only top 5 needed
                ] 
    
    list_top_authors_w_sources_others = [list_top_authors[i] + ', ' + list_top_authors_sources_others[i] 
                                    for i in range(min(len(list_top_authors_sources_others),5))]
    
    return list_top_authors_w_sources_others