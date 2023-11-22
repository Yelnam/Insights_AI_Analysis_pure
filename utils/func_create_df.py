# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:10:19 2022

@author: rober
"""
import pandas as pd
import requests
from lxml import etree
from datetime import datetime
import os

df_temp = pd.DataFrame()

# %% create df from RSS
# create a pandas df from XML data sourced from an RSS feed
def df_from_RSS(url):
    # function expects RSS feed containing: Article ID, Media Type, Category, URL, Date Published, Date Delivered, ...
    # ... Author, Publication, Headline, Full Text
    # formatted as per RSS feed created in Reputation Platform

    response = requests.get(url)

    # parse the XML response content
    root = etree.fromstring(response.content)

    data = []

    for item in root.xpath('//item'):
        
        print(item)
        
        article_id_node = item.find('kmplusItem:idClip', item.nsmap)
        article_id = article_id_node.text if article_id_node is not None else None

        media_type_node = item.find('kmplusItem:medium', item.nsmap)
        media_type = media_type_node.text if media_type_node is not None else None

        category = item.xpath('category/text()')
        category = category[0] if category is not None else None

        url_node = item.find('kmplusItem:contentlink', item.nsmap)
        url = url_node.text if url_node is not None else None

        date_pub_node = item.find('pubDate')
        if date_pub_node is not None:
            date_pub = datetime.strptime(date_pub_node.text, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            date_pub = None
        
        date_del_node = item.find('kmplusItem:deliveredDate', item.nsmap)
        if date_del_node is not None:
            date_del = datetime.strptime(date_del_node.text, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            date_del = None
        
        author_node = item.find('kmplusItem:author', item.nsmap)
        author = author_node.text if author_node is not None else None

        publication_node = item.find('kmplusItem:source', item.nsmap)
        publication = publication_node.text if publication_node is not None else None

        headline_node = item.find('title')
        headline = headline_node.text.strip() if headline_node is not None else None

        full_text_node = item.find('kmplusItem:fulltext', item.nsmap)
        full_text = full_text_node.text if full_text_node is not None else None

        data.append([article_id, media_type, category, url, date_pub, date_del, author, publication, headline, full_text])

    try:
        df = pd.DataFrame(data, columns=['Article ID', 'Media Type', 'Category', 'Url', 'Date Pub', 'Date Del', 'Author', 'Publication', 'Headline', 'Full Text'])
        return df
    
    except Exception as e:
        print("An error occurred while constructing the DataFrame:", str(e))
        return None

# %% create dataframe, top authors --------------------------------------------

# separates out and cleans authors to prep for count and reach calculations

def create_df_top_authors(dataframe = df_temp):
    # filter original df to remove poorly formatted authors
    df_clean_authors = dataframe[dataframe['Author Format Issue'] == False]

    # remove one additional author which is simply '.'
    #     this can't be removed with other symbols as it can be legit part of name
    df_clean_authors = df_clean_authors[df_clean_authors['Author'] != '.']
    
    # create df with value counts of authors
    df_top_authors = df_clean_authors['Author'].value_counts().reset_index()

    # rename columns (older and newer versions of pandas produce different column names. standardise them here)
    df_top_authors.columns = ['Author', 'count']
    
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

# %% create dataframe, top authors by count -----------------------------------

def create_df_top_authors_counts(dataframe = df_temp):
    
    df_top_authors = create_df_top_authors(dataframe)
    # do a new value counts on the resulting table to add same authors together
    df_top_authors_counts = (df_top_authors.groupby('Author', as_index=False)
                                           ['count'].sum()
                                           .sort_values('count', ascending=False)
                                           )

    # rename columns (older and newer versions of pandas produce different column names. standardise them here)
    df_top_authors_counts .columns = ['Author', 'Volume']
    
    return df_top_authors_counts

# %% create dataframe, top authors by reach -----------------------------------

def create_df_top_authors_reach(author_list, reach_list):
    df_top_authors_reach = (pd.DataFrame({'Author': author_list,'Reach': reach_list})
                             .sort_values('Reach', ascending=False)) # creates a df with all authors and their reaches
    
    df_top_authors_reach_legit = [i for i in df_top_authors_reach['Author'] if len(i) > 5]
    
    df_top_authors_reach = df_top_authors_reach[df_top_authors_reach['Author'].isin(df_top_authors_reach_legit)]

    
    return df_top_authors_reach

# %% create dataframe, author sources -----------------------------------------

# generates a df of top sources by volume for a given author

def create_df_author_sources(dataframe = df_temp, author = 'Default Author'):
    df_author_sources = (dataframe['Publication'][dataframe['Author'] == author]
    .value_counts().reset_index()
    .rename(columns={'index': 'Publication', 'Publication': 'Volume'}))
    
    return df_author_sources

