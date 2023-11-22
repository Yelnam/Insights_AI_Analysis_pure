# %% imports

import numpy as np
import pandas as pd

import os
import re
import random
import time
import requests
from lxml import etree
from datetime import datetime
from openpyxl import load_workbook

import openai
from OpenAIKey import open_ai_key
openai.api_key = open_ai_key

from static.prompts import eval_prompt_NICE
from utils.func_dummy_response import generate_dummy_response
from utils.dicts_data_analysis import dict_brand_source, dict_brand_file, dict_brand_RSS_url, dict_brand_prompt, dict_brand_brands
from utils.func_create_df import df_from_RSS
from utils.func_data import brand_consolidator
from utils.func_JSON_to_cols import json_to_cols

# %% In line (non-imported) functions
dict_gpt = {
    '3': 'gpt-3.5-turbo',
    '4': 'gpt-4'
}

# Function - Brand search
# Define the function to search for the brands
def search_brand(text, brand, existing_brands):
    if bool(re.search(r'\b' + re.escape(brand) + r'\b', str(text), flags=re.IGNORECASE)):
        if existing_brands:
            return existing_brands + "|" + brand
        else:
            return brand
    return existing_brands

"""
def standardize_brands_lloyds(brand_string):
    brand_list = brand_string.split('|')
    standardized_brands = ['Lloyds Bank' if brand in ['Lloyds Banking Group', 'Lloyds Bank', 'LBG'] else brand for brand in brand_list]
    return '|'.join(set(standardized_brands))

def standardize_brands_sugar(brand_string):
    brand_list = brand_string.split('|')
    standardized_brands = ['Lord Alan Sugar' if brand in ['Lord Sugar', 'Alan Sugar'] else brand for brand in brand_list]
    return '|'.join(set(standardized_brands))
"""

# %% inputs

# Inputs
model_analyst = dict_gpt[input("Choose GPT model: ")]
sample_rows = input("Choose number of articles to sample. Enter 'All' to analyse full dataset: ")
company = input("Name of company: ")

# %% Data import

# choose whether to import from Excel or XML/RSS

if dict_brand_source[company] == "Excel":
    filename = dict_brand_file[company]
    df = pd.read_excel(filename, engine='openpyxl', sheet_name='Data_to_analyse')
    df_brands = pd.read_excel(filename, engine='openpyxl', sheet_name='Brands_list')

elif dict_brand_source[company] == "RSS":
    df = df_from_RSS(dict_brand_RSS_url[company])
    # expect RSS feed to return many items empty or missing full text. this will remove them from new df
    df = df[(df['Full Text'].notnull()) & (df['Full Text'] != '')]
    brands = dict_brand_brands[company]
    df_brands = pd.DataFrame(brands, columns=['Brands'])

print(f'\ndf length: {len(df)}')
print(f'\ndf: {df}')

# %% Brand search/entity extraction

# Run Brand search on df - three stages
# 1 Search for the brands in the specified column
column_name = 'Full Text'
brand_names = list(df_brands['Brands'])
print("Brand names: ", brand_names, "\n\n")

# 2 Initialise the Brands column
df['Brands_Bool'] = ''

# 3 Loop through brand_names and search for each in the Full Text column, adding found Brands to Brands_Bool column
for brand in brand_names:
    df['Brands_Bool'] = df.apply(
        lambda row: search_brand(row[column_name], brand, row['Brands_Bool']),
        axis = 1                    
        )
    # print(df['Brands_Bool'])


# %% Company-specific settings
"""
# Additional line of code for NICE, which takes all name mentions and simplifies them to NICE
# Values for simplfying might look like: NICE|National Institute for Health and Care Excellence
if company == 'NICE':
    df['Brands_Bool'] = df['Brands_Bool'].apply(lambda x: 'NICE' if pd.notnull(x) else x)

# Similar for LLoyds. Relies on function defined earlier
if company == 'Lloyds Bank':
    df['Brands_Bool'] = df['Brands_Bool'].apply(lambda x: standardize_brands_lloyds(x))

# Similar for Lord Sugar. Relies on function defined earlier
if company == 'Lord Sugar':
    df['Brands_Bool'] = df['Brands_Bool'].apply(lambda x: standardize_brands_sugar(x))
"""
brand_consolidator(company, df)

# %% df reduction

# Create a new df with only articles containing Brand mentions

# Create a separate df containing only rows with Brands in Full Text
df_found_brands = df[df['Brands_Bool'].str.len() > 0]

# Below section generates a sample of articles from the df to send to GPT for analysis
# Sampling is important as it allows a user to test the system before running analysis on a full dataset
# Sample value can be set to All by the user in order to analyse an entire dataset

# Refit sample_rows to size of df_brands if necessary
# sample_rows is the integer number of articles to be analysed by GPT, selected and entered by the front end user
# df_found_brands is the df of all articles in which brand names have been identified
# Therefore it is necessary here to resize sample_rows to ensure the number is not larger than the number of rows in df_found_brands
print("\nArticle analysis: ")
if sample_rows == "All":
    sample_rows = len(df_found_brands)
    print(f"User selected All items - {sample_rows} articles will be analysed by {model_analyst}\n")
elif int(sample_rows) > len(df_found_brands):
    sample_rows = len(df_found_brands)
    print(f"Sample size chosen larger than dataset, user value refitted to data - {sample_rows} articles will be analysed by {model_analyst}\n")
else:
    sample_rows = int(sample_rows)
    print(f"User sample volume successful - {sample_rows} articles will be analysed by {model_analyst}\n")

# Get sample_rows number of random rows from df_found_brands to test

# Get random index rows by taking a sample of sample_rows (variable with integer assigned) from a list of the index values
df_brands_sample_rows = random.sample([i for i in df_found_brands.index], sample_rows)

sample_input = input('Testing only, enter comma separated article indices to evaluate or "x" to use existing set: ')
df_brands_sample_rows = list(map(int, sample_input.split(','))) if sample_input != "x" else df_brands_sample_rows

sample_rows = len(df_brands_sample_rows)

print(f'\nSample row index(s): {df_brands_sample_rows}\n')

# create the sample df with only indices selected at random in the line above
df_brands_sample = df_found_brands[df_found_brands.index.isin(df_brands_sample_rows)]

# %% Generate prompts and responses

# List of prompts, one per article. prompt chosen depends on value assigned to company key in dict_brand_prompt
prompt_list = [dict_brand_prompt[company](df_brands_sample, i) for i in range(len(df_brands_sample))]

# Empty list of responses to be filled later and added to table as new column
response_list = []

# Initialise number of articles analysed at 1, to be iterated with each call to GPT
articles_analysed = 1
start_time = time.time()

prompt_cost_tally = []
response_cost_tally = []
total_cost_tally = []

# Iterate over the items in prompt_list, sending each to GPT for analysis and recording each response on the end of response_list
for i in range(len(prompt_list)):
    try:
        response = openai.ChatCompletion.create(
            model=model_analyst,
            messages=[
                {"role": "system", "content": "You are an experienced media analyst who always returns responses in plain JSON format with no additional commentary."},
                {"role": "user", "content": prompt_list[i]}
            ]
        )
        
    except:
        response = str(generate_dummy_response(company))

    elapsed_time = round(time.time() - start_time, 2)

    print(f"{response}") # check that response is well-formatted. no problems with GPT4, but can be occasionally imperfect with 3

    response_list.append(response['choices'][0]['message']['content'])

    # print(f"response: {response['choices'][0]['message']['content']}")
    print("\n")
    prompt_tokens = response['usage']['prompt_tokens']
    if model_analyst == 'gpt-4':
        prompt_tokens_cost = round( (prompt_tokens/1000) * 0.03 , 4)
    if model_analyst == 'gpt-3.5-turbo':
        prompt_tokens_cost = round( (prompt_tokens/1000) * 0.0015 , 4)
    print(f"prompt tokens: {prompt_tokens}\n")
    print(f"prompt cost: ${prompt_tokens_cost}\n")
    completion_tokens = response['usage']['completion_tokens']
    if model_analyst == 'gpt-4':
        completion_tokens_cost = round( (completion_tokens/1000) * 0.06 , 4)
    if model_analyst == 'gpt-3.5-turbo':
        completion_tokens_cost = round( (completion_tokens/1000) * 0.002 , 4)
    print(f"completion tokens: {completion_tokens}\n")
    print(f"completion cost: ${completion_tokens_cost}\n")
    total_call_cost = prompt_tokens_cost + completion_tokens_cost
    print(f"total call cost: ${total_call_cost}")
    print("\n")
    print(f'Response is of type {type(response)}')
    print("\n")
    print(f"Progress: {articles_analysed} of {sample_rows} articles analysed, Time elapsed: {elapsed_time} seconds \n")

    prompt_cost_tally.append(prompt_tokens_cost)
    response_cost_tally.append(completion_tokens_cost)
    total_cost_tally.append(total_call_cost)

    prompt_cost_sum = round(sum(prompt_cost_tally), 4)
    response_cost_sum = round(sum(response_cost_tally), 4)
    total_cost_sum = round(sum(total_cost_tally), 4)

    print(f'Batch prompt cost total: ${prompt_cost_sum}')
    print(f'Batch response cost total: ${response_cost_sum}')
    print(f'Batch cost total: ${total_cost_sum}\n')
        
    articles_analysed += 1

# Add the prompts and responses to new columns in the sample df
# Use iloc formatting to avoid warnings
df_brands_sample.loc[:, 'Prompt'] = prompt_list
df_brands_sample.loc[:, 'Response'] = response_list

# Reduce the df to only the required columns, for human readability
df_brands_sample = df_brands_sample[['Article ID', 'Media Type', 'Category', 'Url', 'Date Pub', 'Author', 'Publication', 'Headline', 'Full Text', 'Brands_Bool', 'Prompt', 'Response']]

# Transpose the field values from the JSON responses to new columns in the dataframe
df_brands_sample_full = json_to_cols(df_brands_sample, company)

# %% Generate Excel with analysed dataframes

# Generate formatted current date and time (used in filename, this ensures that each filename is unique and won't overwrite previous files produced by the script)
# If temporary file desired in order to avoid filling a directory, remove date string from excel_filename (users will download and save unique file from front end anyway)3
dt_string = str(datetime.now().strftime("%Y %m %d, %H-%M-%S"))

# Create Excel file for export
excel_filename = f'Onclusive_GPT_Auto_Analysis, {company}, {sample_rows} items, {model_analyst} - {dt_string}, {elapsed_time} seconds, P${prompt_cost_sum}, C${response_cost_sum}, T${total_cost_sum}.xlsx'
excel_filepath = os.path.join('outputs', 'Excel_Outputs', excel_filename)            
writer = pd.ExcelWriter(excel_filepath, engine='xlsxwriter')

# Write dfs to Excel on separate Worksheets
df.to_excel(writer, sheet_name = 'Data_All') # dataframe that was imported at start of process from Excel file provided by user
df_found_brands.to_excel(writer, sheet_name = 'Data_Brands_only') # dataframe is exactly the same as Data_All, but contains only rows where one or more brands identified
df_brands_sample_full.to_excel(writer, sheet_name = 'Analysed_articles') # dataframe with GPT analysis added to new metric columns on right of table

# Save document
writer.close()
print('Excel file output to folder')