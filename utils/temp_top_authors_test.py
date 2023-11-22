# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:10:19 2022

@author: rober
"""
import pandas as pd
from lists_data_to_ppt import list_auth_format

df = pd.read_excel('Data_Three_Analysed_GPT4.xlsx',
                            sheet_name='Analysed_articles',
                            header=0,
                            skiprows=0)

df['Author'] = [str(i) for i in df['Author']] # set all authors as str to avoid int or float errors
df['Author'] = [i.strip() for i in df['Author']] # removing leading/trailing spaces
df['Author'] = [i.title() for i in df['Author']] # put authors in title case
df['Author'] = ['Unattributed' if i == 'Nan' else i for i in df['Author'] ]
df['Author Format Issue'] = [any(ele in df['Author'][i] for ele in list_auth_format) for i in range(len(df.index))] # adding column to mark badly formatted Authors, based on list of elements

# %% create dataframe, top authors --------------------------------------------

# separates out and cleans authors to prep for count and reach calculations
def create_df_top_authors(dataframe = df):
    # filter original df to remove poorly formatted authors
    df_clean_authors = dataframe[dataframe['Author Format Issue'] == False]

    # remove one additional author which is simply '.'
    #     this can't be removed with other symbols as it can be legit part of name
    df_clean_authors = df_clean_authors[df_clean_authors['Author'] != '.']
    
    # create df with value counts of authors
    df_top_authors = df_clean_authors['Author'].value_counts().reset_index().rename(columns={'index': 'Author', 0: 'count'})

    print(df_top_authors)
    
    # replace ';' or ' and ' with | so all co-authors are separated in same way
    df_top_authors['Author'] = [i.replace(';', '|') for i in df_top_authors['Author']]
    df_top_authors['Author'] = [i.replace(' and ', '|') for i in df_top_authors['Author']]
    df_top_authors['Author'] = [i.replace(' And ', '|') for i in df_top_authors['Author']]
    df_top_authors['Author'] = [i.replace(' & ', '|') for i in df_top_authors['Author']]
    
    # split authors concatenated with a | 
    df_top_authors['Author'] = [i.split('|') for i in df_top_authors['Author']]
    
    # add split authors to new rows if more than one author on row
    df_top_authors = df_top_authors.explode('Author')
    
    # strip leading and trailing spaces from author names
    df_top_authors['Author'] = [i.strip() for i in df_top_authors['Author']]
    
    # put all authors in Title Case
    df_top_authors['Author'] = [i.title() for i in df_top_authors['Author']]
    
    print(df_top_authors)
    return df_top_authors

create_df_top_authors()