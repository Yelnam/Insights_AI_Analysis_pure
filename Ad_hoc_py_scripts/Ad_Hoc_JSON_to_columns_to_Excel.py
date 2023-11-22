import pandas as pd
import json

df = pd.read_excel("Data_Disney_Analysed_GPT4_working.xlsx",
                        sheet_name='Analysed_articles',
                        header=0,
                        skiprows=0)

print(df.head())


metrics = ['Article_type', 'Mention_YN', 'Corporate_Consumer', 
           'Sentiment', 'Sentiment_explanation', 'Prominence', 
           'Topics', 'Positive_Brand_Values', 'Negative_Brand_Values',
           'Brand_Spokespeople', 'Other_Spokespeople', 'Story']  

# Function to convert json to dict
def json_to_dict(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Could not decode: {json_str}")
        return json_str

# Function to convert any other objects passed as strings
def string_to_dict(row):
    if isinstance(row, str):
        return {}
    else:
        return row

# For handling errors if metric_to_column encounters an error e.g. a mismatched key
def handle_error(row, metric):
    try:
        response = row['Response']
        if isinstance(response, str) and response.strip() == "":
            return "Error filling columns from Response, Brand may be missing from Response"
        else:
            return row['Response'][row['Brand']][metric]
    except Exception as e:
        print(f"Error while handling row: {row}")  # Print the row that caused the error
        print(f"Exception: {e}")  # Print the exception message
        return ""

# Function to convert the JSON returned by GPT into a series of metrics in unique df columns
def json_to_cols(df):   

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
        
    for metric in metrics:
        metric_to_column(metric)

    return df_exploded


df = json_to_cols(df)

print(df['Story'].head())

# Write new dfs to Excel on separate Worksheets
excel_filepath = 'C:/Users/rober/Desktop/Work/1_Automation/O_GPT_Excel_Mod4/outputs/Excel_Outputs/export_dataframe.xlsx'
df.to_excel(excel_filepath, index=False)

print(f"File saved to {excel_filepath}")