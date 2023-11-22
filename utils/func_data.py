# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 11:32:18 2022

@author: rober
"""
import pandas as pd
import json
import ast
import nltk
from nltk.util import ngrams
nltk.download('punkt')
import re
from collections import Counter
from utils.func_create_df import create_df_top_authors_counts, create_df_author_sources
from utils.dicts_data_analysis import dict_brand_brands_2

df_temp = pd.DataFrame() # used on functions defined long ago to supply a temporary df, to be overwritten when df supplied to arg

def search_brand(text, brand, existing_brands):
            if bool(re.search(r'\b' + re.escape(brand) + r'\b', str(text), flags=re.IGNORECASE)):
                if existing_brands:
                    return existing_brands + "|" + brand
                else:
                    return brand
            return existing_brands

def deduplicate_articles(df):

    # take a table containing articles that are in some instances duplicated over multiple rows
    # with minor differences (e.g. diff spokespeople, as per GI output)
    # return a table with only unique articles, where any values that differ between duplicates are turned into pipe-separated concatenates

    def concatenate_unique(x):
        # Convert all elements to string, filter out nan values, use set to ensure unique values, and then join by pipe
        return '|'.join(sorted(set(map(str, x[pd.notna(x)]))))
    
    # Group by 'Article ID' and aggregate
    df_deduplicated = df.groupby('Article ID').agg(concatenate_unique).reset_index()

    return df_deduplicated

def brand_consolidator(company, df, dict_brand_brands_2):

    def reduce_brands(brand_string):
        brands = brand_string.split('|')
        result = []

        # Iterate through key-value pairs in the dictionary for the specified company
        for brand_group, variants in dict_brand_brands_2[company].items():
            for variant in variants:
                if variant in brands:
                    result.append(brand_group) # Append the key (sub-brand) instead of the variant
                    break  # Move on to the next brand group once a match is found

        return '|'.join(result)

    df['Brands_Bool'] = df['Brands_Bool'].apply(reduce_brands)
    
def cost_calculator (response, dict_model_costs, model, articles_analysed, sample_rows, elapsed_time, prompt_cost_tally, response_cost_tally, total_cost_tally):

    # keeps a running total of costs for prompts, completions, and totals, and print out results

    # response_printout = f'Response from {model}: {response}' # debugging check that response is well-formatted. no problems with GPT4, but can be occasionally imperfect with 3
    # print("\n")

    prompt_tokens = response['usage']['prompt_tokens']
    prompt_tokens_cost = round( (prompt_tokens/1000) * dict_model_costs[model]['prompt'] , 4)
    print(f"Current article analysis:\n\nprompt tokens: {prompt_tokens}")
    print(f"prompt cost: ${prompt_tokens_cost}")

    completion_tokens = response['usage']['completion_tokens']
    completion_tokens_cost = round( (completion_tokens/1000) * dict_model_costs[model]['completion'] , 4)
    print(f"completion tokens: {completion_tokens}")
    print(f"completion cost: ${completion_tokens_cost}\n")

    total_call_cost = prompt_tokens_cost + completion_tokens_cost
    print(f"total call cost: ${total_call_cost}")
    print("\n")
    print(f'GPT response is of type {type(response)}')
    print("\n")
    print(f"Progress: {articles_analysed + 1} of {sample_rows} articles analysed, Time elapsed: {elapsed_time} seconds \n")

    # append costs for this article to each list to keep a running tally
    prompt_cost_tally.append(prompt_tokens_cost)
    response_cost_tally.append(completion_tokens_cost)
    total_cost_tally.append(total_call_cost)

    # get a sum of each list
    prompt_cost_sum = round(sum(prompt_cost_tally), 4)
    response_cost_sum = round(sum(response_cost_tally), 4)
    total_cost_sum = round(sum(total_cost_tally), 4)
    
    # print out the running total of costs
    print(f'Running total for this analysis batch:\n\nBatch prompt cost total: ${prompt_cost_sum}')
    print(f'Batch response cost total: ${response_cost_sum}')
    print(f'Batch cost total: ${total_cost_sum}\n')
    
    return prompt_cost_sum, response_cost_sum, total_cost_sum

def assign_prominence(company, list_of_brands, list_of_HLs, list_of_texts):
    
    prominences = []
    prom_summary = []
    word_counts = []
    indices = []
    
    article_no = 1
    
    for brand, headline, text in zip(list_of_brands, list_of_HLs, list_of_texts):
        
        # Remove special characters and links
        clean_text = re.sub(r'\[\/?sourcelink\]|https?:\/\/\S+', '', text)

        # divide text into paragraphs, sentences and words
        paras = clean_text.split('\n')
        sentences = nltk.sent_tokenize(clean_text)
        words = clean_text.split()
        sentence_words = [sentence.split() for sentence in sentences]

        # get article word count
        total_words = len(words)

        # get variations of the brand name from dict_brand_brands_2
        brand_varns = dict_brand_brands_2[company][brand]
        
        # find the length of the longest brand name variation
        var_max_len_brand = max(len(variation.split()) for variation in brand_varns)
        
        # set var_max_len to the minimum of var_max_len_brand and total_words (edge case where text snippets might be shorter than longest name var)
        var_max_len = min(var_max_len_brand, total_words)
        
        # only proceed with creating n-grams if var_max_len is greater than 0
        if var_max_len > 0:
            # create n-grams of the cleaned text
            text_ngrams = [" ".join(gram) for gram in ngrams(clean_text.split(), var_max_len)]

        # index sentence with a 1 if it mentions the brand, 0 if not
        # for the brand supplied to the function (which will be the brand in the Brand column of the article, applied whenever regex search identifies a brand mention)
        # this line will index the each sentence with a 1 if any of its name variations in dict_brand_brands_2 are mentioned
        HL_indexer_brand =          [1 if any(brand_varn.lower() in headline.lower() for brand_varn in brand_varns) else 0]
        paras_indexer_brand =       [1 if any(brand_varn.lower() in para.lower() for brand_varn in brand_varns) else 0 for para in paras]
        sentences_indexer_brand =   [1 if any(brand_varn.lower() in sentence.lower() for brand_varn in brand_varns) else 0 for sentence in sentences]
        words_indexer_brand =       [1 if any(brand_varn.lower() in word.lower() for brand_varn in brand_varns) else 0 for word in words]
        ngram_indexer_brand =       [1 if any(brand_varn.lower() in ngram.lower() for brand_varn in brand_varns) else 0 for ngram in text_ngrams]

        # return a list of indices indicating word (ngram) positions where the brand is mentioned
        ngram_indices = [i for i, val in enumerate(ngram_indexer_brand) if val == 1]
        ngram_indices_str = ", ".join(map(str, ngram_indices))

        # divide text into two equal halfs (for top half/bottom half assignment)
        # currently done on ngrams but could be done on paras if preferred
        half_text = int(len(words)/2)
        top_half = ngram_indexer_brand[:half_text] 
        bottom_half = ngram_indexer_brand[half_text:] 

        # divide each sentence into words, and get a count of words per sentence
        sentence_words = [sentence.split() for sentence in sentences]
        sentences_word_counter = [len(sentence) for sentence in sentence_words]

        # get a sum of word counts for sentences that mention the brand
        # multiply each sentence length by the index (1 or 0) and take the sum of the results
        brand_sentence_words = [a*b for a,b in zip(sentences_indexer_brand, sentences_word_counter)]
        brand_sentence_words_sum = sum(brand_sentence_words)

        # get the Noopsis % by dividing word count of sentences which mention brand over total word counts
        # used only as a criterion for categorising Passing Mentions
        pct = round(brand_sentence_words_sum / total_words * 100 , 2)  

        # assign category based on where brand first appears (will only check next condition is previous fails)
        if HL_indexer_brand[0] == 1: # if brand in headline, assign Headline
            prominence = 'Headline'
        elif paras_indexer_brand[0] == 1: # if brand in first element of paras, assign First paragraph
            prominence = 'First paragraph'
        elif sum(top_half) > 0: # if at least one mention in top half, assign Top Half
            prominence = 'Top half'

        # passing mention not currently active, left to GPT
        # all other categories are strict whereas this one is interpretable and thus better handled by AI
        # existing prominence will be overwritten by Passing Mention if identified by AI

        elif sum(bottom_half) > 0: # if more than one mention in bottom half (and not already assigned Passing mention), assign Bottom Half
            prominence = 'Bottom half'
        else: # if all above cases fail, assign No mention
            prominence = 'No mention'

        article_summary = f'Article {article_no}: {prominence}'
        
        prominences.append(prominence)
        prom_summary.append(article_summary)
        word_counts.append(total_words)
        indices.append(ngram_indices_str)
        
        article_no += 1
    
    return prominences, prom_summary, word_counts, indices

def assign_prominence_pcts(company, list_of_brands, list_of_HLs, list_of_texts):

    # function to assign prominence by 20 percentiles when text paragraph formatting not available
    
    prominences = []
    prom_summary = []
    
    article_no = 1
    
    for brand, headline, text in zip(list_of_brands, list_of_HLs, list_of_texts):
        
        # Remove special characters and links
        clean_text = re.sub(r'\[\/?sourcelink\]|https?:\/\/\S+', '', text)

        # divide text into sentences and words (no paras as we are not expecting them)
        sentences = nltk.sent_tokenize(clean_text)
        words = clean_text.split()
        sentence_words = [sentence.split() for sentence in sentences]

        # get article word count
        total_words = len(words)

        # get variations of the brand name from dict_brand_brands_2
        brand_varns = dict_brand_brands_2[company][brand]
        
        # find the length of the longest brand name variation
        var_max_len_brand = max(len(variation.split()) for variation in brand_varns)
        
        # set var_max_len to the minimum of var_max_len_brand and total_words (edge case where text snippets might be shorter than longest name var)
        var_max_len = min(var_max_len_brand, total_words)
        
        # only proceed with creating n-grams if var_max_len is greater than 0
        if var_max_len > 0:
            # create n-grams of the cleaned text
            text_ngrams = [" ".join(gram) for gram in ngrams(clean_text.split(), var_max_len)]

        # index sentence with a 1 if it mentions the brand, 0 if not
        # for the brand supplied to the function (which will be the brand in the Brand column of the article, applied whenever regex search identifies a brand mention)
        # this line will index the each sentence with a 1 if any of its name variations in dict_brand_brands_2 are mentioned
        HL_indexer_brand =          [1 if any(brand_varn.lower() in headline.lower() for brand_varn in brand_varns) else 0]
        sentences_indexer_brand =   [1 if any(brand_varn.lower() in sentence.lower() for brand_varn in brand_varns) else 0 for sentence in sentences]
        ngram_indexer_brand =       [1 if any(brand_varn.lower() in ngram.lower() for brand_varn in brand_varns) else 0 for ngram in text_ngrams]

        # divide text into two equal halfs (for top half/bottom half assignment)
        # currently done on ngrams but could be done on paras is preferred
        text_quarter = int(len(words)/4)

        pct_0_25 = ngram_indexer_brand[:text_quarter] 
        pct_25_50 = ngram_indexer_brand[text_quarter * 1:text_quarter * 2] 
        pct_50_75 = ngram_indexer_brand[text_quarter * 2:text_quarter * 3] 
        pct_75_100  = ngram_indexer_brand[text_quarter * 3:] 

        # assign category based on where brand first appears (will only check next condition is previous fails)
        if HL_indexer_brand[0] == 1: # if brand in headline, assign Headline
            prominence = 'Headline'
        elif sum(pct_0_25) > 0: # if at least one mention in first 20% of text
            prominence = 'Top quarter'
        elif sum(pct_25_50) > 0: 
            prominence = 'Top half'
        elif sum(pct_50_75) > 0: 
            prominence = 'Bottom half'
        elif sum(pct_75_100) > 0: 
            prominence = 'Bottom quarter'
        else: # if all above cases fail, assign No mention
            prominence = 'No mention'

        article_summary = f'Article {article_no}: {prominence}'
        
        prominences.append(prominence)
        prom_summary.append(article_summary)
        
        article_no += 1
    
    return prominences, prom_summary

def assign_prominence_no_paras(company, list_of_brands, list_of_HLs, list_of_texts):

    # function to assign prominence by 20 percentiles when text paragraph formatting not available
    
    prominences = []
    prom_summary = []
    
    article_no = 1
    
    for brand, headline, text in zip(list_of_brands, list_of_HLs, list_of_texts):
        
        # print(list_of_brands, list_of_HLs, list_of_texts)
        
        # Remove special characters and links
        clean_text = re.sub(r'\[\/?sourcelink\]|https?:\/\/\S+', '', text)

        # divide text into sentences and words (no paras as we are not expecting them)
        sentences = nltk.sent_tokenize(clean_text)
        words = clean_text.split()
        sentence_words = [sentence.split() for sentence in sentences]

        # get article word count
        total_words = len(words)

        # debugging
        print (brand)
        
        # get variations of the brand name from dict_brand_brands_2
        brand_varns = dict_brand_brands_2[company][brand]
        
        # find the length of the longest brand name variation
        var_max_len_brand = max(len(variation.split()) for variation in brand_varns)
        
        # set var_max_len to the minimum of var_max_len_brand and total_words (edge case where text snippets might be shorter than longest name var)
        var_max_len = min(var_max_len_brand, total_words)
        
        # only proceed with creating n-grams if var_max_len is greater than 0
        if var_max_len > 0:
            # create n-grams of the cleaned text
            text_ngrams = [" ".join(gram) for gram in ngrams(clean_text.split(), var_max_len)]

        # index sentence with a 1 if it mentions the brand, 0 if not
        # for the brand supplied to the function (which will be the brand in the Brand column of the article, applied whenever regex search identifies a brand mention)
        # this line will index the each sentence with a 1 if any of its name variations in dict_brand_brands_2 are mentioned
        HL_indexer_brand =          [1 if any(brand_varn.lower() in headline.lower() for brand_varn in brand_varns) else 0]
        sentences_indexer_brand =   [1 if any(brand_varn.lower() in sentence.lower() for brand_varn in brand_varns) else 0 for sentence in sentences]
        ngram_indexer_brand =       [1 if any(brand_varn.lower() in ngram.lower() for brand_varn in brand_varns) else 0 for ngram in text_ngrams]

        # divide text into two equal halfs (for top half/bottom half assignment)
        # currently done on ngrams but could be done on paras is preferred
        text_quarter = int(len(words)/4)

        pct_0_25 = ngram_indexer_brand[:text_quarter] 
        pct_25_50 = ngram_indexer_brand[text_quarter * 1:text_quarter * 2] 
        pct_50_100 = ngram_indexer_brand[text_quarter * 2:] 

        # assign category based on where brand first appears (will only check next condition is previous fails)
        if HL_indexer_brand[0] == 1: # if brand in headline, assign Headline
            prominence = 'Headline'
        elif sum(pct_0_25) > 0: # if at least one mention in first 20% of text
            prominence = 'Top quarter'
        elif sum(pct_25_50) > 0: 
            prominence = 'Top half'
        elif sum(pct_50_100) > 0: 
            prominence = 'Bottom half'
        else: # if all above cases fail, assign No mention
            prominence = 'No mention'

        article_summary = f'Article {article_no}: {prominence}'
        
        prominences.append(prominence)
        prom_summary.append(article_summary)
        
        article_no += 1
    
    return prominences, prom_summary

def noopsis_replicator(company, list_of_brands, list_of_texts):
    
    pcts = []
    formatted_pcts = []
    noopsis_summary = []
    
    article_no = 1
    
    for brand, text in zip(list_of_brands, list_of_texts):
        
        # Remove special characters and links
        clean_text = re.sub(r'\[\/?sourcelink\]|https?:\/\/\S+', '', text)

        # Split text into sentences
        sentences = nltk.sent_tokenize(clean_text)

        # split text into words
        words = clean_text.split()

        # divide each sentence into words, and get a count of words per sentence
        sentence_words = [sentence.split() for sentence in sentences]
        sentences_word_counter = [len(sentence) for sentence in sentence_words]

        # get variations of the brand name from dict_brand_brands_2
        brand_varns = dict_brand_brands_2[company][brand]

        # index sentence with a 1 if it mentions the brand, 0 if not
        # for the brand supplied to the function (which will be the brand in the Brand column of the article, applied whenever regex search identifies a brand mention)
        # this line will index the each sentence with a 1 if any of its name variations in dict_brand_brands_2 are mentioned
        sentences_indexer_brand = [1 if any(brand_varn in sentence for brand_varn in brand_varns) else 0 for sentence in sentences]

        # get article word count
        total_words = len(words)

        # get a sum of word counts for sentences that mention the brand
        # multiply each sentence length by the index (1 or 0) and take the sum of the results
        brand_words = [a*b for a,b in zip(sentences_indexer_brand, sentences_word_counter)]
        brand_words_sum = sum(brand_words)
        
        # get the Noopsis % by dividing word count of sentences which mention brand over total word count
        noopsis_pct = round(brand_words_sum / total_words * 100 , 2)     

        # generate a summary for the article, to be appended to list and printed to console
        # print later removed, can be accessed through return value noopsis_summary if required outside of function
        article_summary = f'Article {article_no}: {noopsis_pct}%'
        
        # categorise brand prominence according to noopsis_pct
        if sum(sentences_indexer_brand) == 1 and noopsis_pct < 20:  # apply Sentence if brand is mentioned in just one sentence
            formatted_pct = 'Sentence'                              # and the sentence comprises less than 20% of the item (for testing, can adjust threshold later if required)
        elif 80 <= noopsis_pct:                                     # else apply category dependent solely on threshold boundaries
            formatted_pct = '80% to 100%'
        elif 50 <= noopsis_pct < 80:
            formatted_pct = '50% to 80%'
        elif 25 <= noopsis_pct < 50:
            formatted_pct = '25% to 50%'
        elif 10 <= noopsis_pct < 25:
            formatted_pct = '10% to 25%'
        elif 0 < noopsis_pct < 10:
            formatted_pct = '<10%'
        else:
            formatted_pct = '0%'
        
        pcts.append(noopsis_pct)
        formatted_pcts.append(formatted_pct)
        noopsis_summary.append(article_summary)
        
        # iterate article number (used in article_summary
        article_no += 1
    
    return pcts, formatted_pcts, noopsis_summary

def column_counter(dict_brand_dfs, brands_present, metric):

    # generate a dictionary containing value counts for a given metric, for each brand present

    dict_brand_values = {}
            
    for brand in brands_present:
        all_values = []
        values = dict_brand_dfs[brand][metric]
        
        for value in values:
            if isinstance(value, str):              # check if the topic is a string
                if value != 'NA':                   # if it's not 'NA'
                    if value.startswith('['):       # if the string is a list
                        value = ast.literal_eval(value)   # parse it back into a list
                        all_values.extend(value)    # add all topics to the list
                    else:
                        all_values.append(value)    # add the topic to the list
        
        count = Counter(all_values)                 # use Counter to count the occurrence of each topic
        dict_brand_values[brand] = count            # add the count to the dictionary

    return dict_brand_values

def count_brand_sentiments(df, column):

    # count sentiment splits for all brands in a df
    # now defunct and replaced with (I think) column_counter

    brands_dict = {}
    
    for index, row in df.iterrows():
        brand_sentiments = row[column].split('|')
        
        for brand_sentiment in brand_sentiments:
            brand, sentiment = brand_sentiment.split(': ')
            if brand not in brands_dict:
                brands_dict[brand] = [0, 0, 0, 0]  # Total, Positive, Neutral, Negative
                
            brands_dict[brand][0] += 1  # Increment total count
            
            if sentiment == "Positive":
                brands_dict[brand][1] += 1
            elif sentiment == "Neutral":
                brands_dict[brand][2] += 1
            elif sentiment == "Negative":
                brands_dict[brand][3] += 1
                
    return brands_dict

def val_counts_try_except(data_column):
    try:
        return data_column.value_counts().reset_index().iloc[0,0]
    except:
        return 'N/A'
     
def get_author_top_source(dataframe = df_temp, author = 'Default Author'):

    # get the source in which a given author appeared most often

    df_author_sources = create_df_author_sources(dataframe, author)
    author_top_source = df_author_sources.iloc[0,0]
    author_top_source_others = (df_author_sources.iloc[0,0]
    if len(df_author_sources) == 1
    else df_author_sources.iloc[0,0]  + ' & others')
    
    return author_top_source, author_top_source_others

def create_monthly_authors_pubs(dataframe, list_months):
    # quick list on monthly top authors
    
    # outdated and much less accurate than simply using create_df_top_authors on each month, as below
    """
    list_monthly_authors_1 = [dataframe['Author'][dataframe['Month'] == i]
                             .value_counts().reset_index().iloc[0,0]
                             if i in list_months
                             else 'NA'
                             for i in range(1,13)]
    
    # list of second author (in case top author is 'Unattributed')
    list_monthly_authors_2 = [dataframe['Author'][dataframe['Month'] == i]
                             .value_counts().reset_index().iloc[1,0]
                             if i in list_months
                             else 'NA'
                             for i in range(1,13)]
    
    # combining lists to use second author when top is 'Unattributed'
    list_monthly_authors = [list_monthly_authors_1[i]
                            if list_monthly_authors_1[i] != 'Unattributed' 
                            else list_monthly_authors_2[i] 
                            for i in range(0,12)]
    """

    list_monthly_authors = [create_df_top_authors_counts(dataframe[dataframe['Month'] == i]).iloc[0,0]
    if i in list_months
    else 'NA'
    for i in range(1,13)]
    
    # list of dataframes of top pubs for all authors in list_monthly_authors
    list_monthly_authors_pub_dfs = [dataframe['Publication']
                                 [(dataframe['Month'] == i+1) 
                                  & (dataframe['Author'] == list_monthly_authors[i])
                                  ].value_counts().reset_index()
                                 for i in range(0,12)]
    
    # list: top publication if top two pub vols !=, else 'various'
    # outdated. for loop below does the same job better
    """list_monthly_authors_pubs = [list_monthly_authors_pub_dfs[i].iloc[0,0]
                            if len(list_monthly_authors_pub_dfs[i].index) < 2 
                            else list_monthly_authors_pub_dfs[i].iloc[0,0]
                            if list_monthly_authors_pub_dfs[i].iloc[0,1] != 
                            list_monthly_authors_pub_dfs[i].iloc[1,1]
                            else 'various'
                            for i in range(0,12)]
    """
    
    list_monthly_authors_pubs = []
    for i in range(0,12):
        try: # try comparing the volumes of the top two publications. if vol in top row is higher, append pub in 1st row
            if len(list_monthly_authors_pub_dfs[i]) == 1: # if df contains only one row
                list_monthly_authors_pubs.append(list_monthly_authors_pub_dfs[i].iloc[0,0])
            elif list_monthly_authors_pub_dfs[i].iloc[0,1] != list_monthly_authors_pub_dfs[i].iloc[1,1]:
                list_monthly_authors_pubs.append(list_monthly_authors_pub_dfs[i].iloc[0,0])
            else: # if vols in top two rows are equal and no clear top source, append 'various'
                list_monthly_authors_pubs.append('various')
        except: # if the above generates an error (eg dataframe only contains one row) then append pub in first row
            list_monthly_authors_pubs.append('NA')
            
    list_monthly_authors_and_pubs_text = [list_monthly_authors[i] + 
                                          ', ' + 
                                          list_monthly_authors_pubs[i]
                                          for i in range(0,12)]
    
    # fill in any missing months with NA
    list_monthly_authors_and_pubs_text
    
    return(list_monthly_authors_and_pubs_text)