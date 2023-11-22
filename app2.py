# %% imports
from flask import Flask, request, render_template, jsonify, send_from_directory, abort, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import re
import openai
import json
import random
import zipfile
import time

from collections import Counter
from datetime import datetime
from openpyxl import load_workbook
from werkzeug.utils import secure_filename

from OpenAIKey import open_ai_key

from static.prompts import eval_prompt_general, eval_prompt_single
from static.asst_model import asst_model
from static.org_chart import org_chart

from utils.func_dummy_response import generate_dummy_response, generate_dummy_response_2
from utils.dicts_data_to_ppt import (dict_company_names, dict_company_logos, dict_company_colors, dict_hl_exclusion, 
                       dict_media_colors, dict_month_to_text, dict_allowed_inputs, dict_low_numbers)
from utils.dicts_data_analysis import dict_brand_brands, dict_brand_brands_2, dict_brand_spokes, dict_brand_SA_cols, dict_brand_metrics_SA, dict_brand_prompt, dict_model_costs
from utils.func_add_charts import add_trend_chart, add_simple_pie, clustered_bar_noX, clustered_bar_noX_cats, clustered_bar_noX_sources
from utils.func_add_text import (add_text, add_text_EOY2022_title, add_text_EOY2022_header, add_text_EOY2022_body, 
                           add_text_EOY2022_topline, add_text_EOY2022_chart_decor, add_text_EOY2022_summary, 
                           add_text_EOY2022_m_side_headers, add_text_EOY2022_top_source,
                           add_text_EOY2022_top_author, add_text_EOY2022_headlines,
                           add_text_author_by_vol, add_text_author_by_reach,
                           add_text_source_by_vol, add_text_source_by_reach)
from utils.func_chatbot import dict_func_args, find_employee, find_lang_speakers
from utils.func_create_df import df_from_RSS, create_df_top_authors, create_df_top_authors_counts, create_df_author_sources, create_df_top_authors_reach
from utils.func_create_list import get_top_source, create_list_top_authors_w_sources, create_list_top_authors_w_sources_others
from utils.func_create_slides import (create_slide_front, create_slide_authors, create_slide_sources, 
                                      create_slide_corp_con, create_slide_sentiment, create_slide_prominence,
                                      create_slide_topics, create_slide_pos_values, create_slide_neg_values, create_slide_spokespeople)
from utils.func_data import (search_brand, brand_consolidator, assign_prominence, assign_prominence_pcts, assign_prominence_no_paras, 
                             noopsis_replicator, cost_calculator, val_counts_try_except, get_author_top_source, 
                        create_monthly_authors_pubs, count_brand_sentiments, column_counter)
from utils.func_format_charts import format_y_axis, apply_data_labels
from utils.func_format_tables import (table_title_height, format_table_alt_color, 
                                format_media_text_color, format_breakdown_table_text,
                                format_media_types_table)
from utils.func_generate_headlines import generate_headlines
from utils.func_inputs import input_checker
from utils.func_JSON_to_cols import json_to_cols, json_to_dict
from utils.func_num_format import rounder, rounder_long
from utils.func_ppt import set_reverse_categories, SubElement, set_cell_border

from utils.lists_data_to_ppt import list_auth_format

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

# % settings
pd.options.display.float_format = '{:.0f}'.format # python specific - force console readout to avoid scientific notation
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script

# %% OpenAI settings

openai.api_key = open_ai_key
# defaults set here, overridden by user inputs for bulk, single and ppt GPT responses
model_full = 'gpt-4' #'code-davinci-002' # 'text-davinci-003' # 'gpt-3.5-turbo'  
model_single = 'gpt-4'
model_ppt = 'gpt-3.5-turbo'
model_chat = "gpt-3.5-turbo"
max_tok = 2000
temp = 0

# %% Flask 

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# %% Route - /download
# Note on download functions below (download_file and download_ppt):
# These functions are essentially exactly the same. The first is for the Excel file returned after running a bulk analysis, the second is for the PowerPoint file
# They use slightly different methods for getting the file, and the first includes explicit error checking (Flask would carry this out anyway so it's implicit in the second)
# Either one could be re-written to resemble the other for consistency
@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if filename is not None:
        try:
            return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'Excel_Outputs'), filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        abort(404)


# %% Route - / (bulk analysis)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # collect inputs
        model_full = request.form.get('model_full')
        model_long = 'gpt-3.5-turbo-16k' if model_full == 'gpt-3.5-turbo' else 'gpt-4' # update when 32K available
        data_source = request.form.get('data_source')
        company = request.form.get('company')
        del_or_pub = request.form.get('del_or_pub')
        year = request.form.get('year')
        month = request.form.get('month')
        sample_rows = request.form.get('sample_rows')
        sample_type = request.form.get('sample_type')
        language = request.form.get('lang')

        if sample_type == None or sample_type == '':
            sample_type = 'rand_n'

        if language == None or language == '':
            language = 'English'

        # set Month name using imported dict_month_to_text dictionary
        month_text = dict_month_to_text[int(month)][1]
        print(f"Month text: {month_text}\n ")

        fileGI = request.files['fileGI']

        if fileGI:
            # Save the file to disk
            filename = secure_filename(fileGI.filename)
            fileGI.save(filename)
            
            # Now read it using pandas
            df_GI = pd.read_excel(filename, engine='openpyxl', sheet_name='GI Export')
            # df_brands = pd.read_excel(filename, engine='openpyxl', sheet_name='Brands_list') # no longer needed. all brands for clients taken from dict_brand_brands

            # Print confirmation
            print('Excel chosen as source. GI file uploaded, and df created')
        
        # Error message if file upload fails
        else:
            return jsonify({'error': 'File processing failed'}), 500
        
        fileSA = request.files['fileSA']

        if fileSA:
            # Save the file to disk
            filename = secure_filename(fileSA.filename)
            fileSA.save(filename)
            
            # Now read it using pandas
            df_SA = pd.read_excel(filename, engine='openpyxl', sheet_name='Sheet1')
            # df_brands = pd.read_excel(filename, engine='openpyxl', sheet_name='Brands_list') # no longer needed. all brands for clients taken from dict_brand_brands

            # Print confirmation
            print('Excel chosen as source. GI file uploaded, and df created')
        
        # Error message if file upload fails
        else:
            return jsonify({'error': 'File processing failed'}), 500
        
        df_GI['Date Pub'] = pd.to_datetime(df_GI['Date Pub'], format='%d/%m/%Y')
        
        # reduce df_GI to month and year specified by user
        # note that datasets do not currently include delivered date, as they're taken from Global Insights/RSS feeds
        df_GI['Month'] = pd.DatetimeIndex(df_GI['Date Pub']).month if del_or_pub == 'P' else pd.DatetimeIndex(df_GI['Delivered']).month
        df_GI['Year'] = pd.DatetimeIndex(df_GI['Date Pub']).year if del_or_pub == 'P' else pd.DatetimeIndex(df_GI['Delivered']).year
        df_GI = df_GI[df_GI['Month'] == int(month)] 
        df_GI = df_GI[df_GI['Year'] == int(year)]

        # fill Full Text in any duplicate rows where it is missing
        df_GI['Full Text'] = df_GI.groupby('Local Article Id')['Full Text'].transform(lambda x: x.fillna(method='ffill').fillna(method='bfill'))

        # then remove any remaining items with no Full Text at all
        df_GI = df_GI[(df_GI['Full Text'].notnull()) & (df_GI['Full Text'] != '')]
                    
        print("df_GI Head:\n\n", df_GI.head)

        # If client Lord Sugar, use Topics to identify whether Lord Sugar or Apprentice mention
        if company == 'Lord Sugar':
            df_GI['Brands_Bool'] = df_GI['Topics']

        # Otherwise run Brand search on df_GI
        else:
            column_name = 'Full Text'
            brand_names = [variation for brand_list in dict_brand_brands_2[company].values() for variation in brand_list]
            print("Brand names:\n\n", brand_names, "\n\n")

            df_GI['Brands_Bool'] = ''

            for brand in brand_names:
                df_GI['Brands_Bool'] = df_GI.apply(
                    lambda row: search_brand(row[column_name], brand, row['Brands_Bool']),
                    axis = 1                    
                    )
                # print(df_GI['Brands_Bool'])

        # print(f'\n\n\n\n\nBrands_Bool head before brand_consolidator: {df_GI["Brands_Bool"].head(5)}\n\n\n\n\n')

        # print(f'\n\n\n\n\nBrands_Bool head after brand_consolidator: {df_GI["Brands_Bool"].head(5)}\n\n\n\n\n')

        df_GI_found_brands = df_GI[df_GI['Brands_Bool'].str.len() > 0]

        # consolidate brands which used more than one search term (e.g. Lloyds Bank, Lloyds Banking Group, LBG > Lloyds Banking Group)
        brand_consolidator(company, df_GI_found_brands, dict_brand_brands_2)

        # Add spokespeople
        column_name = 'Full Text'
        brand_spokes = [variation for brand_list in dict_brand_spokes[company].values() for variation in brand_list]
        print("Brand spokes:\n\n", brand_spokes, "\n\n")

        df_GI_found_brands['Spokespeople'] = ''

        for spokes in brand_spokes:
            df_GI_found_brands['Spokespeople'] = df_GI_found_brands.apply(
                lambda row: search_brand(row[column_name], spokes, row['Spokespeople']),
                axis = 1                    
                )

        # debugging. print cols 
        print(f'\n\n\ndf_GI_found_brands cols: {df_GI_found_brands.columns}\n\n\n')

        # Below section generates a sample of articles from the df_GI to send to GPT for analysis
        print("\nArticle analysis: ")
        if sample_rows == "All":
            sample_rows = len(df_GI_found_brands)
            print(f"User selected All items - {sample_rows} articles will be analysed by {model_full}\n")
        elif int(sample_rows) > len(df_GI_found_brands):
            sample_rows = len(df_GI_found_brands)
            print(f"Sample size chosen larger than dataset, user value refitted to data - {sample_rows} articles will be analysed by {model_full}\n")
        else:
            sample_rows = int(sample_rows)
            print(f"User sample volume successful - {sample_rows} articles will be analysed by {model_full}\n")

        if sample_type == "last_n":
            # Sort the DataFrame by date in descending order (most recent first)
            df_GI_found_brands_sorted = df_GI_found_brands.sort_values(by='Date Pub', ascending=False)

            # Select the top n rows (most recent articles)
            df_GI_brands_sample = df_GI_found_brands_sorted.head(sample_rows)

        # available on front end but not yet active, requires an additional entry box to appear when selected
        # elif sample_type == "i_d":
        
        #     # create a list of Article IDs from a string of comma-separated IDs supplied by the user
        #     user_ID_list = [id.strip() for id in sample_input.split(',')] 

        #     # create the sample df with only indices selected in the line above
        #     df_GI_brands_sample = df_GI_found_brands[df_GI_found_brands['Article ID'].isin(user_ID_list)]


        else: # if sample type is rand_n, or if no value is entered, sample at random
            df_GI_brands_sample = df_GI_found_brands.sample(n=sample_rows)

        # print(f'\n\n\ndf_GI_brands_sample cols: {df_GI_brands_sample.columns}\n\n\n')

        # Generate responses from GPT 

        # prompt depends on clients for a set of pre-defined clients. otherwise general prompt will be used
        # if company in dict_brand_prompt:
        #     prompt_list = [dict_brand_prompt[company](df_GI_brands_sample, i, language) for i in range(len(df_GI_brands_sample))]
        # else:
        #     prompt_list = [eval_prompt_general(df_GI_brands_sample, i, language) for i in range(len(df_GI_brands_sample))]

        # Create list of prompts depending on length of Full Text
        prompt_list = [eval_prompt_general(company, df_GI_brands_sample, dict_brand_brands_2, i, language) for i in range(len(df_GI_brands_sample))]

        # print(f'\n\n\n\n\nprompt_list: {prompt_list}\n\n\n\n\n')

        response_list = []
        articles_analysed = 0
        start_time = time.time()
        prompt_cost_tally = []
        response_cost_tally = []
        total_cost_tally = []

        # %% Send to GPT
        for i in range(len(prompt_list)):
            try:
                response = openai.ChatCompletion.create(
                    model=model_full,
                    messages=[
                        {"role": "system", "content": "You are an experienced media analyst who always returns responses in plain JSON format with no additional commentary."},
                        {"role": "user", "content": prompt_list[i]}
                    ]
                )
                
            except:
                response = generate_dummy_response_2()

            elapsed_time = round(time.time() - start_time, 2)
            response_list.append(response['choices'][0]['message']['content'])

            prompt_cost_sum, response_cost_sum, total_cost_sum = cost_calculator (response, dict_model_costs, model_full, 
                                                                                  articles_analysed, sample_rows, elapsed_time, 
                                                                                  prompt_cost_tally, response_cost_tally, total_cost_tally)
            
            articles_analysed += 1

        print(f'\n\n\ndf_GI_brands_sample cols2: {df_GI_brands_sample.columns}\n\n\n')        

        # Add the prompts and responses to new columns in the sample df
        df_GI_brands_sample.loc[:, 'Prompt'] = prompt_list
        df_GI_brands_sample.loc[:, 'Response'] = response_list

        # Reduce the df_GI to only the required columns, for human readability
        df_GI_brands_sample = df_GI_brands_sample[['Local Article Id', 'Url', 'Headline', 'Full Text', 'Brands_Bool', 'Spokespeople', 'Response', 'Topics']]

        # Transpose the field values from the JSON responses to new columns in the dataframe
        df_GI_brands_sample_full = json_to_cols(df_GI_brands_sample, company)

        print(f'\n\n\ndf_GI_brands_sample_full cols: {df_GI_brands_sample_full.columns}\n\n\n')  
        
        list_of_brands = [i for i in df_GI_brands_sample_full['Brand']]
        list_of_HLs = [i for i in df_GI_brands_sample_full['Headline']]
        list_of_texts = [i for i in df_GI_brands_sample_full['Full Text']]

        # Get values for the percentage Prominence column (and a printable summary)
        column_prominence_pcts, summary_prominence_pcts = assign_prominence_no_paras(company, list_of_brands, list_of_HLs, list_of_texts)

        # Assign new columns to analysed df
        df_GI_brands_sample_full['Prominence_pct'] = column_prominence_pcts
        df_GI_brands_sample_full['Prominence'] = np.where(df_GI_brands_sample_full['Passing_mention'] == 'Yes', 'Passing mention', df_GI_brands_sample_full['Prominence_pct'])
        
        # Select only columns that we want to add to the df_SA
        df_GI_brands_sample_reduced = df_GI_brands_sample_full[dict_brand_metrics_SA[company]]
        df_GI_brands_sample_reduced = df_GI_brands_sample_reduced.rename(columns={'Local Article Id': 'ArticleId'})

        # Drop the columns from df_SA
        df_SA = df_SA.drop(dict_brand_SA_cols[company], axis=1)

        # Debugging - remove later
        for col in df_GI_brands_sample_reduced.columns:
            print(col)
    
        for col in df_SA.columns:
            print(col)

        # Merge new columns onto df_SA base
        df_combined = pd.merge(df_SA, df_GI_brands_sample_reduced, on='ArticleId', how='outer', validate='1:m')

        # %% Generate Excel with analysed dataframes
        dt_string = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

        # get costs in cents to add to filename
        prompt_cents = round(prompt_cost_sum * 100, 2)
        completion_cents = round(response_cost_sum * 100, 2)
        total_cents = round(total_cost_sum * 100, 2)

        # Create Excel file for export
        excel_filename = (f'Automated_Analysis_{company}, {sample_rows} items, {model_full}, L={language}, {elapsed_time} seconds, '
        f'P{prompt_cents}c, C{completion_cents}c, T{total_cents}c, {dt_string}.xlsx')

        excel_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Excel_Outputs', excel_filename)            
        writer = pd.ExcelWriter(excel_filepath, engine='xlsxwriter')

        # Write dfs to Excel on separate Worksheets
        df_GI_brands_sample_reduced.to_excel(writer, sheet_name = 'Analysed_articles') 
        df_combined.to_excel(writer, sheet_name = 'Combined dfs') 

        # Save document
        writer.close()
        print('Excel file output to folder')
 
        return jsonify({'filename': excel_filename, 
                        'prompt_cents': prompt_cents, 'completion_cents': completion_cents, 'total_cents': total_cents,
                        'elapsed_time': elapsed_time, 'articles_analysed': articles_analysed})
    
    # Return value needed to generate index.html web front end
    return render_template('index2.html')  
    


# %% if name main
# Ensures that script only runs if directly executed (rather than called from another script)
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'outputs'  # Set the upload folder
    app.run(debug=True)