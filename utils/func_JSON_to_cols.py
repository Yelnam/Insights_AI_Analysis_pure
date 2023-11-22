import pandas as pd
import json
from datetime import datetime
from utils.dicts_data_analysis import dict_brand_metrics, dict_brand_metrics_cols

# Function to convert json to dict
def json_to_dict(json_str):
    try:
        json_str = json_str.strip('`')
        json_str = json_str.replace("json\n", "")
        json_str = json_str.strip()
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e, "for json string:", json_str)
        return None

# Function to convert any other objects passed as strings
def string_to_dict(row):
    if isinstance(row, str):
        return {}
    else:
        return row

# For handling errors if metric_to_column encounters an error e.g. a mismatched key
logged_articles = set()

def handle_error(row, metric):
    try:
        return row['Response'][row['Brand']][metric]
    except Exception as e:
        article_headline = row["Headline"]
        if article_headline not in logged_articles:
            print(f'Error with metric {metric} while handling row during JSON to cols process. See article: {article_headline}')
            logged_articles.add(article_headline)
        # print(f"Error while handling row: {row}")  # Print the row that caused the error
        # print(f"Exception: {e}")  # Print the exception message
        if metric == "Mention_YN":
            return "Error filling columns from Response, Brand may be missing from Response"
        else:
            return ""


# Function to convert the JSON returned by GPT into a series of metrics in unique df columns
def json_to_cols(df, company):   

    # Split Brands_Bool into a list of brands
    df['Brands_Bool'] = df['Brands_Bool'].str.split('|')
    
    # Convert Response from JSON to dict, IF not dict already
    try:
        df['Response'] = df['Response'].apply(json_to_dict)
    except:
        pass

    # "Explode" the Brands_Bool column to get one row for each brand and article
    df_exploded = df.explode('Brands_Bool')

    # Rename the exploded column to Brand
    df_exploded.rename(columns={'Brands_Bool': 'Brand'}, inplace=True)

    # Extract relevant metrics from Response for each Brand
    def metric_to_column(metric):
        df_exploded[metric] = df_exploded.apply(lambda row: handle_error(row, metric), axis=1)

    metrics = dict_brand_metrics_cols[company]['brand_metrics']   
        
    for metric in metrics:
        metric_to_column(metric)

    return df_exploded
