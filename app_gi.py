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
from utils.dicts_data_analysis import dict_brand_brands, dict_brand_brands_2, dict_brand_spokes, dict_brand_metrics_cols, dict_brand_prompt, dict_model_costs, dict_model_current 
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
from utils.func_data import (search_brand, deduplicate_articles, brand_consolidator, assign_prominence, assign_prominence_no_paras, 
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
model_full = 'gpt-4-1106-preview' # 'gpt-4-1106-preview' 'gpt-4' 'code-davinci-002' # 'text-davinci-003' # 'gpt-3.5-turbo'  
model_single = 'gpt-4-1106-preview'
model_ppt = 'gpt-3.5-turbo'
model_chat = "gpt-3.5-turbo"
max_tok = 2000
temp = 0

# %% Flask 
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# %% Route - /
@app.route('/', methods=['GET'])
def home():
    return render_template('index_gi.html')

# %% Route - /download
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

# %% Route - /download_ppt
@app.route('/download_ppt/<path:filename>', methods=['GET'])
def download_ppt(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'PPT_Outputs'), filename, as_attachment=True)

# %% Route - /chat
messages = [{"role": "system", "content": asst_model}]

@app.route('/chat', methods=['POST'])
def chat():
    global messages  

    message = request.json['message']
    print(f"User: {message}")
    print("Fetching response from Open AI")
    start_time = time.time()

    if message:
        messages.append({"role": "user", "content": message})

        print(messages)

        functions = [
                    {
                        "name": "find_employee",
                        "description": "Find an employee by full or partial name",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "org_chart": {
                                    "type": "object",
                                    "description": "The organization chart",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "The firstname, surname or full name of a member of staff",
                                }
                            },
                            "required": ["org_chart", "name"],
                        },
                    },
                    {
                        "name": "find_lang_speakers",
                        "description": "Find speakers of a given language in the organisation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "org_chart": {
                                    "type": "object",
                                    "description": "The organization chart",
                                },
                                "language": {
                                    "type": "string",
                                    "description": "The language to search for",
                                }
                            },
                            "required": ["org_chart", "language"],
                        },
                    },
                ]
                        
        response = openai.ChatCompletion.create(
            model=model_chat,
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        reply = response['choices'][0]['message']

        print(f'Response: {response}')

        if reply.get("function_call"):
            available_functions = {
                "find_employee": find_employee,
                "find_lang_speakers": find_lang_speakers,
            }
            
            func_name = reply["function_call"]["name"]
            func_to_call = available_functions[func_name]
            func_args = json.loads(reply["function_call"]["arguments"])
            func_response = func_to_call(org_chart=org_chart, **func_args)

            print(f'Function response: {func_response}')

            # Step 4: send the info on the function call and function response to GPT
            messages.append(reply)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": func_name,
                    "content": func_response,
                }
            )  # extend conversation with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )  # get a new response from GPT where it can see the function response

            final_reply = second_response['choices'][0]['message']['content']

            print(f'Final reply: {final_reply}')

            return jsonify(final_reply)
        
        else:
            final_reply = response['choices'][0]['message']['content']

        messages.append({"role": "assistant", "content": final_reply})
        
        elapsed_time = round(time.time() - start_time, 2)
        print(f"Time elapsed: {elapsed_time} seconds")
        
        print(f"Wall-O: {final_reply}")
        print(f"Conversation history: {messages}")
        
        return jsonify(final_reply)


# %% Route - /single
@app.route('/single', methods=['POST'])
def single_article():
    model_single = request.json['modelSingle']
    article_headline = request.json['articleHeadline']
    article_text = request.json['articleText']
    user_brand_list = request.json['brandList']
    user_brand_list = [brand.strip() for brand in user_brand_list.split(",")]
    print(f"Brand list: {user_brand_list},\n Article headline: {article_headline},\n Article start: {article_text[0:100]}")

    start_time = time.time()

    # Using the variables in the prompt
    prompt = (f"The following list is called brand_list: {user_brand_list}\n"
    "The following represents the headline and full text of a news article: \n"

    "Headline: \n"
    f"{article_headline}\n"
    "Article text: \n"
    f"{article_text}"

    # Full prompt imported from prompts.py. 
    f"{eval_prompt_single}"
    )
    print(f"Prompt compiled.\n\n Prompt:\n {prompt}\n\n Fetching response from {model_single}.\n\n")

    response = openai.ChatCompletion.create(
                    model=model_single,
                    messages=[
                        {"role": "system", "content": "You return responses in plain JSON format with no additional commentary."},
                        {"role": "user", "content": prompt}
                    ]
                )
    print(response)

    response_text = response['choices'][0]['message']['content']
    print(response_text)
    
    response_dict = json.loads(response_text)

    elapsed_time = round(time.time() - start_time, 2)
    print(f"Time elapsed: {elapsed_time} seconds")

    return jsonify(response_dict) 


# %% Route - /form (bulk analysis)
@app.route('/form', methods=['GET', 'POST'])
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

        # update to current version of GPT 3 or 4
        model_full = dict_model_current[model_full]

        if sample_type == None or sample_type == '':
            sample_type = 'rand_n'

        if language == None or language == '':
            language = 'English'

        month_text = dict_month_to_text[int(month)][1]
        print(f"Month text: {month_text}\n ")

        if data_source == 'Excel':
            file = request.files['file']

            if file:
                # Save the file to disk
                filename = secure_filename(file.filename)
                file.save(filename)
                
                # Now read it using pandas
                df = pd.read_excel(filename, engine='openpyxl', sheet_name='Export')
                # df_brands = pd.read_excel(filename, engine='openpyxl', sheet_name='Brands_list') # no longer needed. all brands for clients taken from dict_brand_brands

                # Print confirmation
                print('Excel chosen as source. File uploaded, and df created')
        
        elif data_source == 'RSS':
            rss_url = request.form.get('rss_url')
            df = df_from_RSS(rss_url)
            # Print confirmation
            print('RSS chosen as source. URL accessed, and df created')

        else:
            return jsonify({'error': 'File processing failed'}), 500
        
        if data_source == 'Excel':
            try:
                df['Date Pub'] = pd.to_datetime(df['Date Pub'], format='%d/%m/%Y')
            except:
                df['Date Pub'] = pd.to_datetime(df['Date Pub'], format='mixed')

        elif data_source == 'RSS':
            df['Date Pub'] = pd.to_datetime(df['Date Pub'], format='%Y-%m-%d %H:%M:%S')
        
        # reduce df to month and year specified by user
        # note that datasets do not currently include delivered date, as they're taken from Global Insights/RSS feeds
        df['Month'] = pd.DatetimeIndex(df['Date Pub']).month if del_or_pub == 'P' else pd.DatetimeIndex(df['Delivered']).month
        df['Year'] = pd.DatetimeIndex(df['Date Pub']).year if del_or_pub == 'P' else pd.DatetimeIndex(df['Delivered']).year
        df = df[df['Month'] == int(month)] 
        df = df[df['Year'] == int(year)]

        print(f'len df 1: {len(df)}')

        df = df[(df['Full Text'].notnull()) & (df['Full Text'] != '')]
        df_full = df # used later
                    
        print("df Head:\n\n", df.head)
        # print("df_brands:\n\n", df_brands, "\n\n") # df_brands no longer used. brand names printed below

        column_name = 'Full Text'
        brand_names = [variation for brand_list in dict_brand_brands_2[company].values() for variation in brand_list]

        print(brand_names)

        # generate a new column which records whether each brand was discovered in the Full Text via a Boolean-type search (actually regex rather than Boolean)
        df['Brands_Bool'] = ''
        for brand in brand_names:
            df['Brands_Bool'] = df.apply(
                lambda row: search_brand(row[column_name], brand, row['Brands_Bool']),
                axis = 1                    
                )
            # print(df['Brands_Bool'])

        # print(f'\n\n\n\n\nBrands_Bool head before brand_consolidator: {df["Brands_Bool"].head(5)}\n\n\n\n\n')

        print(f'len df 2: {len(df)}')

        # consolidate brands which used more than one search term (e.g. Lloyds Bank, Lloyds Banking Group, LBG > Lloyds Banking Group)
        brand_consolidator(company, df, dict_brand_brands_2)

        print(f'len df 3: {len(df)}')

        # print(f'\n\n\n\n\nBrands_Bool head after brand_consolidator: {df["Brands_Bool"].head(5)}\n\n\n\n\n')

        # Create a separate df with only articles containing Brand mentions
        df_found_brands = df[df['Brands_Bool'].str.len() > 0]

        print(f'len df 4: {len(df_found_brands)}')

        # Below section generates a sample of articles from the df to send to GPT for analysis
        print("\nArticle analysis: ")
        if sample_rows == "All":
            sample_rows = len(df_found_brands)
            print(f"User selected All items - {sample_rows} articles will be analysed by {model_full}\n")
        elif int(sample_rows) > len(df_found_brands):
            sample_rows = len(df_found_brands)
            print(f"Sample size chosen larger than dataset, user value refitted to data - {sample_rows} articles will be analysed by {model_full}\n")
        else:
            sample_rows = int(sample_rows)
            print(f"User sample volume successful - {sample_rows} articles will be analysed by {model_full}\n")

        # NB front end option to supply ArticleIDs for analysis is a placeholder and NOT yet programmed
        if sample_type == "last_n":
            # Sort the DataFrame by date in descending order (most recent first)
            df_found_brands_sorted = df_found_brands.sort_values(by='Date Pub', ascending=False)

            # Select the top n rows (most recent articles)
            df_brands_sample = df_found_brands_sorted.head(sample_rows)

        else: # if sample type is rand_n, or if no value is entered, sample at random
            df_brands_sample = df_found_brands.sample(n=sample_rows)
        
        # Generate responses from GPT 

        # if company in dict_brand_prompt:
        #     prompt_list = [dict_brand_prompt[company](df_brands_sample, i, language) for i in range(len(df_brands_sample))]
        # else:
        #     prompt_list = [eval_prompt_general(df_brands_sample, i, language) for i in range(len(df_brands_sample))]

        prompt_list = [eval_prompt_general(company, df_brands_sample, dict_brand_brands_2, i, language) for i in range(len(df_brands_sample))]

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

        print(f'\n\n\n\n\nPrompt cost sum: {prompt_cost_sum}\n\n\n\n\n')

        # Add the prompts and responses to new columns in the sample df
        # (not sure why I used .loc here as it seems like unnecessary overkill. may have been to avoid generating a warning message)
        df_brands_sample.loc[:, 'Prompt'] = prompt_list
        df_brands_sample.loc[:, 'Response'] = response_list

        # Reduce the df to only the required columns, for human readability
        df_brands_sample = df_brands_sample[['Article ID', 'Media Type', 'Category', 'Url', 'Date Pub', 'Author', 'Publication', 'Headline', 'Full Text', 'Brands_Bool', 'Prompt', 'Response']]
        
        # print df_brands_sample Brands_Bool (temporary debugging step, remove later if not required)
        # print(f'\n\n\n\n\nBrands_Bool head after analysis: {df_brands_sample["Brands_Bool"].head(5)}\n\n\n\n\n')

        # Transpose the field values from the JSON responses to new columns in the dataframe
        df_brands_sample_full = json_to_cols(df_brands_sample, company)

        # Generate prominences from texts
        list_of_brands = [i for i in df_brands_sample_full['Brand']]
        list_of_HLs = [i for i in df_brands_sample_full['Headline']]
        list_of_texts = [i for i in df_brands_sample_full['Full Text']]

        column_prominence, summary_prominence, col_word_counts, col_brand_indices = assign_prominence(company, list_of_brands, list_of_HLs, list_of_texts)

        column_prominence_pcts, summary_prominence_pcts = assign_prominence_no_paras(company, list_of_brands, list_of_HLs, list_of_texts)

        column_Noopsis_raw, column_Noopsis_formatted, summary_Noopsis = noopsis_replicator(company, list_of_brands, list_of_texts)

        print(f'df Columns: {df_brands_sample_full.columns}')

        # Assign new columns to analysed df
        df_brands_sample_full['Word_count'] = col_word_counts
        # df_brands_sample_full['Brand mentions'] = col_brand_indices
        df_brands_sample_full['Prominence_Logical'] = column_prominence
        df_brands_sample_full['Prom_log_x_PM'] = np.where(df_brands_sample_full['Passing_mention'] == 'Yes', 'Passing mention', df_brands_sample_full['Prominence_Logical'])
        # df_brands_sample_full['Line_break_issue'] = df_brands_sample_full.apply(lambda row: 'Issue' if ('\n' not in str(row['Full Text'])) and (row['Word_count'] > 100) else 'No issue', axis=1)
        # df_brands_sample_full['Prominence_pct'] = column_prominence_pcts
        df_brands_sample_full['Prom_Noop_cat'] = column_Noopsis_formatted
        df_brands_sample_full['Prom_Noop_pct'] = column_Noopsis_raw

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
        df_full.to_excel(writer, sheet_name = 'Data_All') 
        df.to_excel(writer, sheet_name = 'Data_Full_Text') 
        df_found_brands.to_excel(writer, sheet_name = 'Data_FT_and_Brand') 
        df_brands_sample_full.to_excel(writer, sheet_name = 'Analysed_articles') 

        # Save document
        writer.close()
        print('Excel file output to folder')

        return jsonify({'filename': excel_filename, 
                        'prompt_cents': prompt_cents, 'completion_cents': completion_cents, 'total_cents': total_cents,
                        'elapsed_time': elapsed_time, 'articles_analysed': articles_analysed})
    

    
# %% Route - /form_gi (bulk analysis from GI)
@app.route('/form_gi', methods=['GET', 'POST'])
def index_gi():
    if request.method == 'POST':
        # collect inputs
        model_full = request.form.get('model_full_gi')
        model_long = 'gpt-3.5-turbo-16k' if model_full == 'gpt-3.5-turbo' else 'gpt-4' # update when 32K available
        company = request.form.get('company_gi')
        del_or_pub = request.form.get('del_or_pub_gi')
        year = request.form.get('year_gi')
        month = request.form.get('month_gi')
        sample_rows = request.form.get('sample_rows_gi')
        sample_type = request.form.get('sample_type_gi')
        language = request.form.get('lang_gi')

        # update to current version of GPT 3 or 4
        model_full = dict_model_current[model_full]

        if sample_type == None or sample_type == '':
            sample_type = 'rand_n'

        if language == None or language == '':
            language = 'English'

        print(f"\n\nAnalysis will use model {model_full}\n ")

        # set Month name using imported dict_month_to_text dictionary
        month_text = dict_month_to_text[int(month)][1]
        print(f"Month to analyse: {month_text}\n ")

        fileGI = request.files['fileGI']

        if fileGI:
            # Save the file to disk
            filename = secure_filename(fileGI.filename)
            fileGI.save(filename)
            
            df_GI = pd.read_excel(filename, engine='openpyxl', sheet_name='Export')
            # df_brands = pd.read_excel(filename, engine='openpyxl', sheet_name='Brands_list') # no longer needed. all brands for clients taken from dict_brand_brands

            # Print confirmation
            print('GI file uploaded and df created')
        
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
            print('SA file uploaded and df created')
        
        # Error message if file upload fails
        else:
            return jsonify({'error': 'File processing failed'}), 500
        
        # ensure correct datetime formatting
        try:
            df_GI['Date Pub'] = pd.to_datetime(df_GI['Date Pub'], format='%d/%m/%Y')
        except:
            df_GI['Date Pub'] = pd.to_datetime(df_GI['Date Pub'], format='mixed')
        
        # reduce df_GI to month and year specified by user
        # note that datasets do not currently include delivered date, as they're taken from Global Insights/RSS feeds
        df_GI['Month'] = pd.DatetimeIndex(df_GI['Date Pub']).month if del_or_pub == 'P' else pd.DatetimeIndex(df_GI['Delivered']).month
        df_GI['Year'] = pd.DatetimeIndex(df_GI['Date Pub']).year if del_or_pub == 'P' else pd.DatetimeIndex(df_GI['Delivered']).year
        df_GI = df_GI[df_GI['Month'] == int(month)] 
        df_GI = df_GI[df_GI['Year'] == int(year)]

        # compress duplicates from GI onto a single line, concatenating with pipes any values that differ between rows
        df_GI = deduplicate_articles(df_GI)
        df_GI_full_deDuped = df_GI # df copy exported at end of process to Excel, for reference

        # fill Full Text in any duplicate rows where it is missing
        #   no longer necessary as all articles are de-duped onto single line
        # df_GI['Full Text'] = df_GI.groupby('Local Article Id')['Full Text'].transform(lambda x: x.fillna(method='ffill').fillna(method='bfill'))

        # then remove any remaining items with no Full Text at all
        df_GI = df_GI[(df_GI['Full Text'].notnull()) & (df_GI['Full Text'] != '')]
                    
        print("\ndf_GI Head:\n\n", df_GI.head(5))

        # If GI output includes a field with brands recorded already, use these
        if dict_brand_metrics_cols[company]['brands_bool'] != 'run':
            print(f'\This client uses brands identified by GI. Brands to analyse will be copied from the GI column {dict_brand_metrics_cols[company]["brands_bool"]}' )
            df_GI['Brands_Bool'] = df_GI[dict_brand_metrics_cols[company]['brands_bool']]

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

        print(f'Debugging: Brands_Bool head before df_GI_found_brands created: {df_GI["Brands_Bool"].head(3)}n\n')

        df_GI_found_brands = df_GI[df_GI['Brands_Bool'].str.len() > 0]

        print(f'\nDebugging: Brands_Bool head before brand_consolidator: {df_GI["Brands_Bool"].head(3)}\n\n')

        print(f'Before brand_consolidator, dataframe df_GI_found_brands is of length: {len(df_GI_found_brands)}')

        # consolidate brands which used more than one search term (e.g. Lloyds Bank, Lloyds Banking Group, LBG > Lloyds Banking Group)
        brand_consolidator(company, df_GI_found_brands, dict_brand_brands_2)

        print(f'\n\nDebugging: Brands_Bool head after brand_consolidator: {df_GI_found_brands["Brands_Bool"].head(3)}\n\n')

        # debugging. print cols 
        # print(f'\n\nDebugging: df_GI_found_brands cols: {df_GI_found_brands.columns}\n\n')

        print(f'After brand_consolidator, dataframe df_GI_found_brands is of length: {len(df_GI_found_brands)}')

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

        print(f'df_GI_brands_sample created, dataframe is of length: {len(df_GI_brands_sample)} (should match number of articles to be evaluated)')

        # print(f'\n\nDebugging: df_GI_brands_sample cols: {df_GI_brands_sample.columns}\n\n')

        # Generate responses from GPT 

        # Create list of prompts depending on length of Full Text
        prompt_list = [eval_prompt_general(company, df_GI_brands_sample, dict_brand_brands_2, i, language) for i in range(len(df_GI_brands_sample))]

        # print(prompt_list)

        print(f'\nChecking brands to be passed to GPT for analysis: \ndf_GI_brands_sample Brands_Bool head - pre-GPT: {df_GI_brands_sample["Brands_Bool"].head()}\n\n')
        # print(f'\n\nprompt_list: {prompt_list}\n\n')

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
        
            print(f'Article {articles_analysed + 1}: Response from {model_full}: {response}')

        print(f'\n\nDebugging: df_GI_brands_sample Brands_Bool head - post_GPT: {df_GI_brands_sample["Brands_Bool"].head()}')

        # print(f'\n\nDebugging: df_GI_brands_sample cols2: {df_GI_brands_sample.columns}\n\n')        

        # Add the prompts and responses to new columns in the sample df
        df_GI_brands_sample.loc[:, 'Prompt'] = prompt_list
        df_GI_brands_sample.loc[:, 'Response'] = response_list

        # Reduce the df_GI to only the required columns, for human readability
        df_GI_brands_sample = df_GI_brands_sample[dict_brand_metrics_cols[company]['GI_cols']]

        # Transpose the field values from the JSON responses to new columns in the dataframe

        print(f'\n\nDebugging: df_GI_brands_sample cols - pre-json: {df_GI_brands_sample.columns}')

        # This was a temporary debugging step for Santander, but should now be redundant
        #   as Banks will be copied to Brands_Bool as per dict_brand_metrics_cols[company]['brands_bool']
        # if company == "Santander":
        #     print(f'\n\n\ndf_GI_brands_sample Banks head - pre-json: {df_GI_brands_sample["Banks"].head()}\n\n\n')

        print(f'\n\ndf_GI_brands_sample Brands_Bool head - pre-json: {df_GI_brands_sample["Brands_Bool"].head(3)}\n\n')

        df_GI_brands_sample_full = json_to_cols(df_GI_brands_sample, company)

        print(f'\n\ndf_GI_brands_sample_full cols - post-json: {df_GI_brands_sample_full.columns}\n\n')  

        ## Add scripted spokespeople (hard coded in dict_brand_spokes)
        # get unique brands from Brand column

        # print(f'Debugging: df_GI_brands_sample_full head, check Brand column for generating found_brands: {df_GI_brands_sample_full.head(5)}')

        found_brands = df_GI_brands_sample_full['Brand'].unique()

        # remove empty values from found_brands
        found_brands = [brand for brand in found_brands if brand]

        # create empty temp df with headers matching df_GI_brands_sample_full
        df_GI_brands_sample_full_temp = pd.DataFrame(columns=df_GI_brands_sample_full.columns)

        print(f'found brands for generating Spokespeople column: {found_brands}\n\n')

        for found_brand in found_brands:
            df_GI_found_brand = df_GI_brands_sample_full[df_GI_brands_sample_full['Brand'] == found_brand]

            # Add spokespeople
            column_name = 'Full Text'
            brand_spokes = [variation for spokes_list in dict_brand_spokes[company][found_brand].values() for variation in spokes_list]
            print("Spokespeople identified for Brand passed to brand_spokes dict:\n", brand_spokes, "\n\n")

            df_GI_found_brand['Spokespeople'] = ''

            for spokes in brand_spokes:
                df_GI_found_brand['Spokespeople'] = df_GI_found_brand.apply(
                    lambda row: search_brand(row[column_name], spokes, row['Spokespeople']),
                    axis = 1
                )
            
            df_GI_brands_sample_full_temp = pd.concat([df_GI_brands_sample_full_temp, df_GI_found_brand], ignore_index=True)

        df_GI_brands_sample_full = df_GI_brands_sample_full_temp
        
        list_of_brands = [i for i in df_GI_brands_sample_full['Brand']]
        list_of_HLs = [i for i in df_GI_brands_sample_full['Headline']]
        list_of_texts = [i for i in df_GI_brands_sample_full['Full Text']]

        # Get values for the percentage Prominence column (and a printable summary)
        column_prominence_pcts, summary_prominence_pcts = assign_prominence_no_paras(company, list_of_brands, list_of_HLs, list_of_texts)

        # Assign new columns to analysed df
        df_GI_brands_sample_full['Prominence_pct'] = column_prominence_pcts
        df_GI_brands_sample_full['Prominence'] = np.where(df_GI_brands_sample_full['Passing_mention'] == 'Yes', 'Passing mention', df_GI_brands_sample_full['Prominence_pct'])
        
        # Select only columns that we want to add to df_SA
        df_GI_brands_sample_reduced = df_GI_brands_sample_full[dict_brand_metrics_cols[company]['brand_metrics_SA']]
        df_GI_brands_sample_reduced = df_GI_brands_sample_reduced.rename(columns={'Local Article Id': 'ArticleId'})

        # Drop the columns from df_SA
        df_SA = df_SA.drop(dict_brand_metrics_cols[company]['SA_cols'], axis=1)

        # Merge new columns onto df_SA base
        df_GI_brands_sample_reduced['ArticleId'] = df_GI_brands_sample_reduced['ArticleId'].astype(int)
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
        df_GI_full_deDuped.to_excel(writer, sheet_name = 'GI_deDuped') 
        df_combined.to_excel(writer, sheet_name = 'Combined_dfs') 

        # Save document
        writer.close()
        print('\nExcel file output to folder\n')
 
        return jsonify({'filename': excel_filename, 
                        'prompt_cents': prompt_cents, 'completion_cents': completion_cents, 'total_cents': total_cents,
                        'elapsed_time': elapsed_time, 'articles_analysed': articles_analysed})
    
 


# %% Route - /generate_ppt
# Defines function for generating PPT from analysed articles

@app.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the file to disk
            filename = secure_filename(file.filename)
            file.save(filename)

            model_ppt = request.form.get('model_ppt')
            company = request.form.get('company')
            del_or_pub = request.form.get('del_or_pub_ppt')
            year = request.form.get('year')
            month = request.form.get('month')
            company_color_yn = request.form.get('company_color_yn')
            company_logo_yn = request.form.get('company_logo_yn')

            print("\nVariables set by user:\n"
                  f"GPT model: {model_ppt}\n"
                  f"Company: {company}\n"
                  f"Delivered or Published: {del_or_pub}\n"
                  f"Year: {year}\n"
                  f"Month: {month}\n"
                  f"Use company color? {company_color_yn}\n"
                  f"Use company logo? {company_logo_yn}\n"
            )

            # set company logo size and position
            # not currently used directly in script. outsourced to slide creation functions
            """
            if company_logo_yn in ['Y','y']: co_logo_left = dict_company_logos[company][0]
            if company_logo_yn in ['Y','y']: co_logo_top = dict_company_logos[company][1]
            if company_logo_yn in ['Y','y']: co_logo_width = dict_company_logos[company][2]
            if company_logo_yn in ['Y','y']: co_logo_height = dict_company_logos[company][3]
            """

            # Get company color from imported dict if user chooses Y for company color
            company_color_from_dict = RGBColor.from_string(dict_company_colors[company]) if company_color_yn in ['Y', 'y'] else None
            company_color = company_color_from_dict if company_color_yn in ['Y', 'y'] else RGBColor(183,136,250)

            month_text = dict_month_to_text[int(month)][1]

            # Company name variations, from imported dict, based on input
            company_title = dict_company_names[company][0] 
            company_full = dict_company_names[company][1] 
            company_short = dict_company_names[company][2]
            company_image = dict_company_names[company][3]
            company_headline = dict_company_names[company][4]
            company_alt = dict_company_names[company][5]
        
            # %% DATAFRAME - IMPORT AND CLEAN -----------------------------------------------------
            df = pd.read_excel(filename,
                            sheet_name='Analysed_articles',
                            header=0,
                            skiprows=0)
            
            print(f"len df after import from front end: {len(df)}")
            print(f"\ndf head after import from front end: \n {df.head()}")

            # DATA FORMATTING AND CLEANING ---------------------------------------
            # This is partial and dependent on the current data

            df['Date Pub'] = pd.to_datetime(df['Date Pub'], dayfirst=True) # ensure all dates set to datetime format
            # ^^ IMPORTANT 1 - dayfirst argument is based on format when using Global Insights export as input. May not work for other input formats
            # ^^ IMPORTANT 2 - Do same for Published date when using dataset containing Published
            print(f'\n"Date Pub" dtype: {df.dtypes["Date Pub"]}\n')
            df['Publication'] = [i.replace(" (Web)", "") if any(ext in i for ext in ['Online', 'online', '.com']) else i for i in df['Publication']]
            df['Publication'] = [i.strip() for i in df['Publication']] # removing leading/trailing spaces from publication
            df['Author'] = [str(i) for i in df['Author']] # set all authors as str to avoid int or float errors
            df['Author'] = [i.strip() for i in df['Author']] # removing leading/trailing spaces
            df['Author'] = [i.title() for i in df['Author']] # put authors in title case
            df['Author'] = ['Unattributed' if i == 'Nan' else i for i in df['Author'] ]
            df['Author Format Issue'] = [any(ele in df['Author'][i] for ele in list_auth_format) for i in range(len(df.index))] # adding column to mark badly formatted Authors, based on list of elements
            
            # Add Month and Year columns using either Published or Delivered date, using P or (else) D as determined by user inputs
            df['Month'] = pd.DatetimeIndex(df['Date Pub']).month if del_or_pub == 'P_ppt' else pd.DatetimeIndex(df['Delivered']).month
            df['Year'] = pd.DatetimeIndex(df['Date Pub']).year if del_or_pub == 'P_ppt' else pd.DatetimeIndex(df['Delivered']).year
            # Printout to check length of df after adding columns
            print(f'len df after adding Month and Year: {len(df)}\n')
            df = df[df['Month'] == int(month)] # filter df by month
            # Printout to check length of df after filtering by Month (and value counts by Month)
            print(f'len df after filter by month: {len(df)}')
            print(f'Value Counts of new Month column: \n{df.Month.value_counts()}\n')
            df = df[df['Year'] == int(year)] # filter df by user-specified year, from input above
            # Printout to check length of df after filtering by Year (and value counts by Year)
            print(f'len df after filter by year: {len(df)}')
            print(f'Value Counts of new Year column: \n{df.Year.value_counts()}')

            print (f"\ndf head after data cleaning:\n {df.head()}\n\n")

            # MINI DATAFRAMES ----------------------------------------------------

            df_top_sources = df['Publication'].value_counts().reset_index()
            df_top_sources.columns = ['Publication', 'Volume']
                                
            print(f"df_top_sources:\n {df_top_sources.head()}")
            
            df_top_authors = create_df_top_authors(dataframe = df) # df containing only cleaned authors
            df_top_authors_counts = create_df_top_authors_counts(df) # runs df_create_top_authors then returns a value count
            df_top_author_sources = pd.DataFrame() # defined lower down

            brands_present = list(df['Brand'].unique())
            # quick function which returns tuples for all brands recording if they are not company (ie the client), and the name of the brand
            def custom_sort(brand):
                return (brand != company, brand)
            brands_present.sort(key=custom_sort)

            print(f'\nbrands_present in order (should be client first, with remainder in AZ order): {brands_present}')


            dict_brand_dfs = {brand: df[df['Brand'] == brand] for brand in brands_present}
            
            
            # %% KEY DATAPOINTS -----------------------------------------------------------


            # sources ------------------------------------------------------------
            # sources by volume -------------------------------------------
            top_source_by_vol = df_top_sources.iloc[0,0]
            top_source_vol = df_top_sources.iloc[0,1]
            try: top_source_top_author = create_df_top_authors_counts(df[df['Publication'] == top_source_by_vol]).iloc[0,0]
            except: top_source_top_author = 'NA'
            try: top_source_top_author_vol = create_df_top_authors_counts(df[df['Publication'] == top_source_by_vol]).iloc[0,1]
            except: top_source_top_author_vol = 'NA'
            list_top_sources_by_vol = df_top_sources['Publication'][0:5]
            list_top_sources_vol = df_top_sources['Volume'][0:5]
            
            # authors ------------------------------------------------------------
            # authors by volume --------------------------------------------
            top_author_by_vol = df_top_authors_counts.iloc[0,0]
            top_author_by_vol_surname = top_author_by_vol.split()[-1]
            top_author_vol = df_top_authors_counts.iloc[0,1]
            top_author_by_vol_source, top_author_by_vol_source_others = get_author_top_source(df, top_author_by_vol)
            list_top_authors = [i for i in df_top_authors_counts['Author']] # run as list comprehension to return list rather than pd series
            list_top_authors_vols = [i for i in df_top_authors_counts['Volume']]
            
            # Generate Topline figures per Metric for each Brand --------------
                       
            # Sentiment
            dict_brand_sentiment = {brand: dict_brand_dfs[brand]['Sentiment'].value_counts() for brand in brands_present}
            print(f"\ndict_brand_sentiment:\n\n {dict_brand_sentiment[company]}")
            
            # Prominence
            dict_brand_prominence = {brand: dict_brand_dfs[brand]['Prominence'].value_counts() for brand in brands_present}
            print(f"\ndict_brand_prominence:\n\n {dict_brand_prominence[company]}")

            # Corporate/Consumer
            dict_brand_corp_con = {brand: dict_brand_dfs[brand]['Corporate_Consumer'].value_counts() for brand in brands_present}
            print(f"\ndict_brand_corp_con:\n\n {dict_brand_corp_con[company]}")
            
            # Topics
            dict_brand_topics = column_counter(dict_brand_dfs, brands_present, 'Topics')
            print(f"\ndict_brand_topics:\n\n {dict_brand_topics[company]}")

            # Spokespeople
            dict_brand_spokespeople = column_counter(dict_brand_dfs, brands_present, 'Spokespeople')
            print(f"\ndict_brand_spokespeople:\n\n {dict_brand_spokespeople[company]}")

            # Positive Brand Values
            dict_brand_pos_values = column_counter(dict_brand_dfs, brands_present, 'Positive_Brand_Values')
            print(f"\ndict_brand_pos_values:\n\n {dict_brand_pos_values[company]}")

            # Negative Brand Values
            dict_brand_neg_values = column_counter(dict_brand_dfs, brands_present, 'Negative_Brand_Values')
            print(f"\ndict_brand_neg_values:\n\n {dict_brand_neg_values[company]}")

            # %% COMMENTARY -------------------------------------------------------------

            # brands text - CURRENTLY STATIC, SET LIVE FOR NON-DUMMY PRODUCT BY GETTING GPT SUMMARIES FOR EACH
                      
            dict_brand_sent_text = {
                "Disney": "In this time period, the Disney+ brand is predominantly presented in a positive or neutral light. Positive sentiments largely arise from its commitment to producing new and diverse content, including its first French original film and new series like 'Les enfants sont rois'. Such developments create anticipation and demonstrate the platform's dedication to international content and diversity, fostering positive sentiment. Meanwhile, neutral mentions reflect Disney+'s role as a hosting platform for various series and documentaries, serving a functional role without generating specific sentiments. There is only one negative mention related to a significant loss of subscribers. Overall, while Disney+ is largely perceived positively for its content offerings, it should address the issue that led to the loss of subscribers to further enhance its reputation.",
                "Three": "Three's media coverage has been mixed. Positive sentiment prevails due to several factors such as their proposed merger with Vodafone potentially forming Britain's largest mobile network operator, successful energy-saving measures in data centres, and advantageous deals available on their network. However, significant negative sentiment has arisen primarily due to plans for 5G mast installations near schools and playgrounds, which have generated community concern. Some price increase announcements have also led to negative sentiment. Additionally, numerous neutral mentions are present, largely concerning merger plans with Vodafone and network aspects.",
                "BT Mobile": "BT Mobile's media coverage portrays it in a negative light, primarily due to a high rate of customer complaints associated with its mobile services. This recurring issue is creating an adverse image for the company in the public eye, impacting its reputation. It appears necessary for BT Mobile to address these concerns to improve its media sentiment and customer satisfaction.",
                "EE": "The sentiment of EE's media coverage is mixed, with neutral mentions being the most frequent. These neutral instances often relate to EE's involvement in industry changes or events, without expressing explicit criticism or praise. However, some negative sentiment is tied to EE due to price increases causing customer discontent. This adverse coverage is somewhat balanced by positive mentions, acknowledging EE's low complaint rates for certain services, innovative 4G connectivity in underserved areas, and the offering of value-adding deals. Overall, EE's media perception appears relatively balanced but fluctuating.",
                "O2": "The sentiment of O2's media coverage is predominantly neutral and positive, with a few instances of negative sentiment. Neutral mentions often relate to industry changes or events, without explicit approval or criticism. Positive sentiment mostly stems from O2's service offerings, including cost-effective deals, early access to events and games, combatting data poverty, and venue hosting. The negative sentiment relates to an upcoming broadband price increase, contributing to some dissatisfaction among customers. The coverage indicates a mostly favorable perception of O2, despite some criticism.",
                "Sky Mobile": "Sky Mobile's media coverage in this period was limited but positive. The sentiment was favourable due to a reported £5 discount on a data plan, reflecting Sky Mobile's provision of good value to its customers. The absence of negative or neutral mentions during this time suggests a positive perception of Sky Mobile in the media.",
                "Smarty": "Smarty's media coverage during this period is predominantly positive, bolstered by the announcement of its new social tariff and a deal offering double the usual data for the same price, highlighting the brand's value proposition. While there are some neutral mentions, tying Smarty as a low-cost brand and an MVNO of Three UK, these neither detract from nor enhance the brand's positive portrayal. Overall, the media sentiment towards Smarty is favourable.",
                "Tesco Mobile": "Tesco Mobile's media sentiment during the assessed period has been overwhelmingly positive. The brand has been recognised for its exceptional customer service, specifically illustrated by its low complaint rate, establishing Tesco Mobile as a commendable performer in the sector.",
                "Virgin Mobile": "During the assessed period, the media sentiment towards Virgin Mobile has been predominantly negative. The brand has been linked with multiple customer dissatisfaction issues, including price increases and the discontinuation of a popular free public WiFi service. Additionally, Virgin Mobile has attracted a significant number of complaints, further tarnishing its reputation in the sector.",
                "Vodafone": "The media sentiment regarding Vodafone over the assessed period has been mixed. The proposed merger with Three UK, which could result in the formation of Britain's largest mobile operator, has been viewed positively and neutrally. Vodafone's role as a partner of The National Databank in an initiative to fight data poverty and enhancing connectivity at the Glastonbury Festival were also noted positively. However, the brand faced criticism due to the upcoming broadband price increase and a high number of complaints received in both the broadband and mobile service segments. Neutral sentiment was associated with infrastructural changes and product availability.",
                "Voxi": "The media sentiment towards Voxi in this period has been neutral. The brand is recognized as a part of Vodafone's portfolio, and it has been suggested that Voxi may need to adopt strategies similar to Three UK. There were no instances of distinctly positive or negative sentiment associated with Voxi during this period."
                }
            
            dict_brand_prom_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Three experienced a balanced spread of media mentions, with almost a quarter in headlines and first paragraphs, a fifth in the top half of articles, and just over a third in the bottom half. Headline coverage was driven largely by the potential £15bn merger with Vodafone, with stories in ISPreview, Digitalisation World, London South East, and Investing.com, amongst others. In the first paragraphs, Three's 5G mast plans drew attention, causing protests and leading to withdrawal of some applications, as reported in Yahoo! UK and Ireland and the Sussex Express. Their agreement with NTT DATA for IT infrastructure overhaul also featured prominently. In the top half of articles, stories ranged from Three's opposition over 5G mast placements to customer service issues reported by Ofcom. The bottom half coverage included topics from Three's early access ticket offers to price hikes and partnerships.",
                "BT Mobile": "During the period, BT Mobile's media presence was extremely minimal, with only a single mention located in the top half of an article. The story was covered by Ofcom's website, under the headline 'Latest telecoms and pay-TV complaints revealed'. The article touched on complaints BT Mobile received, focusing primarily on mobile services. In essence, the narrative around BT Mobile during this period was characterized by a focus on customer service and user experience concerns within the telecoms sector.",
                "EE": "EE had a moderate spread of media mentions with around one-sixth appearing in headlines and first paragraphs, two-fifths in the top half of articles, and a quarter in the bottom half. In headlines, prominent stories included EE's increased data offer for the same price and price hikes due to inflation, reported by Times of Bristol and Daily Express respectively. First paragraph mentions featured on topics such as broadband price increase and explanations on EE's Smart Hub light signals. Top half of articles highlighted EE's plans to phase out 3G and its lower complaint rate, while in the bottom half, the focus was on EE's lack of 5G in certain locations and customer dissatisfaction due to price hikes.",
                "O2": "O2 had balanced media mentions with one-fifth each appearing in headlines, first paragraphs, and the top half of articles, and two-fifths in the bottom half. Headline stories revolved around O2's half-price SIMs with ample data, free early Diablo IV Beta access, and a popular £17 per month iPhone XS contract. The first paragraph mentions highlighted O2 as a UFC 286 venue, a broadband price increase, and benefits from a bundle with Virgin Media. The top half of articles referred to O2 in the context of a potential Vodafone-Three merger and early access to Ticketmaster events. In the bottom half, mentions centered on the lack of 5G in areas and the continuation of underground WiFi services.",
                "Sky Mobile": "Sky Mobile had minimal media presence during this period, with a single mention located in the bottom half of an article in the Times of Bristol. This mention discussed Sky Mobile's new offer, providing a £5 discount on a new data plan, contributing to the narrative of competitive pricing strategies in the mobile telecommunications industry.",
                "Smarty": "During the period, Smarty, the low-cost mobile brand, held a notable headline presence in Computeractive, launching a social tariff for £12/month. This prominence was overshadowed by three occurrences in the bottom half of articles, primarily related to its potential implication in the Vodafone-Three merger. The brand also attracted attention for doubling data for the same price in a deal, as reported by the Times of Bristol.",
                "Tesco Mobile": "Tesco Mobile's presence in the media during this period was solely marked by a mention in the top half of an Ofcom article. This attention was attributed to the brand's low level of customer complaints for its mobile services, positioning Tesco Mobile as a reliable provider in the telecoms sector.",
                "Virgin Mobile": "Throughout the period, Virgin Mobile garnered equal media prominence across headlines, first paragraphs, and the top half of articles. The Times of Bristol headlined with 'Virgin Media reveals more bad news for customers as price rise looms' regarding their price hike and discontinuation of public WiFi. The same story featured in the Daily Express' opening paragraph, further spreading this news. Additionally, Ofcom reported high customer complaints for Virgin Mobile's services, enhancing the brand's negative exposure.",
                "Vodafone": "Vodafone experienced significant media visibility, with over half of its mentions in headlines. Dominating stories included its impending merger with Three UK and a major tariff increase, as reported by ISPreview and Investing.com UK. Its partnership with Samsung to expand Open RAN in Europe and the Emirates-based group increasing their stake in the company also made headlines. In other parts of articles, Vodafone's increased broadband charges, the switch-off of its 3G service, and being the leader in complaints for broadband and mobile services were highlighted.",
                "Voxi": "Voxi's media mentions were limited to the bottom half of articles. Both mentions pertained to the impending merger between Vodafone and Three UK, reported by ISPreview and Mobile Europe. The reports suggest that Voxi, being a part of Vodafone, may need to adjust its strategy in light of the merger."
                }
            
            dict_brand_corp_con_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Three's media mentions were overwhelmingly corporate, accounting for roughly three-quarters of the coverage. Key issues included a potential merger with Vodafone, energy savings in data centres, and backlash against proposed 5G masts near schools and playgrounds. These topics drove mentions in outlets like ISPreview, Digitalisation World, and local news sites. On the consumer side, which made up around a quarter of the mentions, themes centred on pricing changes, early access to events for Three customers, and high complaint rates, as reported by Times of Bristol and Ofcom among others.",
                "BT Mobile": "During the reporting period, all media mentions of BT Mobile were consumer-focused. Predominantly, the brand was mentioned in the context of customer complaints, primarily for its mobile services. This was noted in an article on the Ofcom website, which placed the mention in the top half of the article.",
                "EE": "For EE, the balance of media coverage during the reporting period leaned more towards corporate (around 60%) than consumer (around 40%). Corporate mentions were driven by issues like planned 3G phase-out, price hikes and strategic decisions related to network improvement. Consumer coverage highlighted topics such as EE's data offers, customer complaints and explanations about their products like the Smart Hub. The increase in broadband prices and EE's customer dissatisfaction due to inflation were key issues appearing in both corporate and consumer mentions.",
                "O2": "Media mentions for O2 were nearly equally divided between corporate and consumer topics. Corporate headlines focused on O2's planned broadband price increase and its role in the broader UK telecom landscape, notably in relation to the proposed Vodafone-Three merger. The telecom's corporate aspects were cited in Caithness Business Index and Mobile Europe, among others. On the consumer side, stories spotlighted O2's enticing deals like half-price SIMs and an affordable iPhone XS contract, along with early game and event access perks. Consumer mentions appeared in the Times of Bristol and The Sun Online, among other outlets.",
                "Sky Mobile": "Sky Mobile had minimal media coverage during the reporting period, with just one consumer-centric mention. As reported by the Times of Bristol, the brand offered a £5 discount on a new data plan, aiming to provide more affordable options for consumers in the competitive mobile service market. The lack of corporate mentions suggests a quiet period for Sky Mobile in corporate developments or initiatives.",
                "Smarty": "In the reporting period, Smarty was mainly in consumer-focused news, marking around three-quarters of its media mentions. The brand launched a social tariff and doubled data for the same price, attracting consumer attention. However, its corporate identity was also recognized as being a part of the potential Vodafone-Three UK merger due to its position as a low-cost brand, accounting for about a quarter of its overall coverage. This mixed coverage indicates Smarty's dual role as an affordable consumer choice and an influential corporate player.",
                "Tesco Mobile": "During the reporting period, Tesco Mobile's sole mention, found in a consumer-focused publication, showcased its high customer satisfaction. According to Ofcom, the brand has been applauded for having the fewest complaints about mobile services. This underlines Tesco Mobile's strong consumer-focused service and quality, as reflected by the positive customer feedback.",
                "Virgin Mobile": "Virgin Mobile had three consumer-related mentions, focusing on price hikes and discontinuation of public WiFi, revealed in Times of Bristol and Daily Express. This has led to negative sentiment, as indicated by Ofcom's report of high complaint rates for mobile services. The brand is facing consumer dissatisfaction due to increased prices and service changes, adversely affecting its reputation.",
                "Vodafone": "Vodafone garnered majority corporate mentions (over 65%) largely centred on its imminent merger with Three UK, as reported by ISPreview and others. Other key topics include a major tariff increase and a partnership with Samsung for Open RAN expansion. On the consumer front, constituting a third of mentions, Vodafone's value propositions were highlighted, like Glastonbury connectivity partnership and affordable data plans, but it also led in broadband and mobile service complaints, according to Ofcom, indicating mixed consumer sentiment.",
                "Voxi": "The media equally mentioned Voxi in corporate and consumer contexts (each 50%). The brand's mentions, both by ISPreview and Mobile Europe, were related to the potential impact of the impending Vodafone and Three UK merger. This major industry event is prompting speculation about Voxi's potential strategy adjustment in response."
                }
            
            dict_brand_topics_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Media coverage of the brand Three was primarily driven by regulatory matters (38%), which included an imminent £15bn merger with Vodafone as reported by ISPreview, and the backlash regarding the brand's proposed 5G masts in areas such as Great Bardfield and Wickford. Offers or deals made up 28% of the coverage, with stories like early access to event tickets for Three customers and contract extensions with partners. The brand's financial performance (15%) also had notable mentions, including energy savings and a possible price increase. New product launches made up the smallest portion (10%) with mentions of Three's collaboration with NTT DATA and Console Connect.",
                "BT Mobile": "The only topic mentioned in media coverage of BT Mobile was Regulation (100%). A report by Ofcom highlighted high complaint rates for BT Mobile's services, leading to a negative sentiment. The key driver for this coverage was evidently consumer dissatisfaction as stated in the Ofcom article's headline 'Latest telecoms and pay-TV complaints revealed'. Hence, the brand's reputation in the media was influenced by regulatory reports, underscoring the need for better customer service.",
                "EE": "The media coverage for the brand EE was distributed fairly evenly across four topics: Financial performance (17%), Regulation (33%), Product launch (25%), and Offers or Deals (25%). Regulatory matters garnered attention as EE received the fewest complaints for broadband and home phone services, according to Ofcom, and it was mentioned in the context of a potential Vodafone-Three merger. Financial performance and Offers or Deals were highlighted in news about price hikes, countered by reports of EE offering increased data for the same price. Coverage on Product Launch was mainly about the EE Smart Hub and the phasing out of 3G services.",
                "O2": "O2's media coverage was mainly about Offers or Deals, making up over half (53%) of the topics, while Regulation was discussed in 20% of the coverage, and Financial Performance and Product Launch each accounted for 7%. Media reports were generally positive, focusing on various cost-effective deals such as half-price SIMs with substantial data and early access to Diablo IV Beta. Regulatory issues were mostly neutral, while Financial Performance saw negative sentiment due to an upcoming broadband price increase. The brand's 5G coverage and its collaboration with Virgin Media also garnered attention.",
                "Sky Mobile": "Sky Mobile's media coverage was exclusively about Offers or Deals, accounting for 100% of the topics. The only mention in the top 50 media discussions focused on a positive sentiment, with the brand providing a £5 discount on a new data plan, indicating a good value proposition to consumers. This was reported in the Times of Bristol, in the bottom half of the article.",
                "Smarty": "Media coverage for the brand Smarty was evenly distributed among Regulation, Product launch, and Offers or Deals, each making up a portion of the coverage. The headline mention in Computeractive highlighted the positive launch of Smarty's social tariff. Meanwhile, ISPreview and Mobile Europe both neutrally reported Smarty's status as a part of Three UK in the context of a potential Vodafone-Three merger. Lastly, Times of Bristol drew attention to Smarty's positive offer of double the usual data for the same price.",
                "Tesco Mobile": "Tesco Mobile's media coverage was entirely focused on Regulation. The brand was mentioned positively by Ofcom, with the reporting highlighting Tesco Mobile's low number of complaints for mobile services, positioning it as a customer-friendly provider in the telecommunications sector.",
                "Virgin Mobile": "Virgin Mobile's media coverage was distributed equally across Financial Performance, Regulation, and Offers or Deals, each making up a third. However, the brand was presented negatively in all instances. This included reports on price hikes and termination of a public WiFi service (Times of Bristol, Daily Express) under Financial Performance and Offers or Deals, and high complaint rates highlighted by Ofcom under Regulation.",
                "Vodafone": "Media coverage of Vodafone was spread across Financial Performance (29%), Regulation (33%), Product Launch (19%), and Offers or Deals (24%). Key mentions included the impending £15bn merger with Three UK (ISPreview, London South East), major tariff increases (Investing.com UK), and partnerships to expand Open RAN in Europe (Vanilla Plus). Also noteworthy were positive comments about data offerings (Times of Bristol) and connectivity at Glastonbury (The Sun). However, there were negatives in the form of high complaint volumes (Ofcom) and upcoming broadband price increases (Caithness Business Index).",
                "Voxi": "Media coverage for Voxi was solely concentrated on Regulation (100%), with no mentions of Financial Performance, Product Launch, or Offers or Deals. Mentioned in the context of Vodafone's impending £15bn merger with Three UK (ISPreview), Voxi was highlighted as a Vodafone brand. Additionally, the brand's potential need to adjust its strategy in response to the merger was also discussed (Mobile Europe)."
            }

            dict_brand_spokespeople_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Placeholder text. Add dynamic text or use GPT to generate.",
                "BT Mobile": "Placeholder text. Add dynamic text or use GPT to generate.",
                "EE": "Placeholder text. Add dynamic text or use GPT to generate.",
                "O2": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Sky Mobile": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Smarty": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Tesco Mobile": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Virgin Mobile": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Vodafone": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Voxi": "Placeholder text. Add dynamic text or use GPT to generate."
            }

            dict_brand_pos_values_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Brand Three's media coverage prominently showcased values of Innovation (25%) and Value (18%). This was primarily driven by the brand's imminent merger with Vodafone, hailed as a notable innovation and widely reported by media outlets such as ISPreview and London South East. The sustainable energy saving measures implemented in their data centres also contributed to the Innovation narrative, covered by Digitalisation World and ACR Today. Value-driven mentions highlighted Three's customer benefits like early access to events and competitive deals, as in Mobile Marketing Magazine and Trusted Reviews. Transparency/Trust, Sustainability, and Inclusivity, although less frequent, were positively mentioned in discussions around partnerships, energy savings, and initiatives to alleviate data poverty.",
                "BT Mobile": "BT Mobile received no media coverage associated with positive brand values such as Design, Innovation, Inclusivity, Sustainability, Transparency/Trust, or Value. The only significant mention of BT Mobile was associated with high complaint rates for its mobile services, as reported by Ofcom, and this did not correspond to any of the defined positive brand values.",
                "EE": "Media coverage of the brand EE highlighted the company's Innovation, Value, and Transparency/Trust. Instances of Innovation were seen in the Railway Herald and Computeractive, with EE offering 4G connectivity in hard-to-reach areas and planning a 3G phase-out. The brand's Value was highlighted in The Times of Bristol and Ofcom, with EE providing increased data deals for the same price and attracting the fewest complaints for broadband and home phone services. Transparency/Trust was emphasised by The Big Tech Question, where the EE Smart Hub's light signals were explained.",
                "O2": "O2's media coverage prominently featured the brand values of Value, Innovation, and Inclusivity. Value was the most frequently occurring value, highlighted in cost-effective deals such as half-price SIMs with good data offers (Times of Bristol) and a budget-friendly iPhone XS contract (The Sun Online). Innovation was evident in offering early access to Diablo IV Beta for its users (ISPreview) and exclusive benefits in a Volt bundle with Virgin Media. O2's Inclusivity was underscored in the Northampton Evening Telegraph, where O2 partnered with The National Databank to combat data poverty.",
                "Sky Mobile": "Sky Mobile's media coverage was primarily focused on the brand value of 'Value'. This was conveyed through the offering of a cost-effective data plan, which was positively received as it incorporated a £5 discount. This was featured in the 'Times of Bristol' publication, indicating a focus on providing customers with affordable mobile plans.",
                "Smarty": "The media representation of Smarty was predominantly centered around the brand value of 'Value' (75%), with 'Innovation' also featuring significantly (25%). This was driven by Smarty's launch of a cost-effective social tariff, and its offer of double data for the same price, as covered by 'Computeractive' and the 'Times of Bristol' respectively. These strategies showcased Smarty's innovative approach and commitment to delivering excellent value to its customers.",
                "Tesco Mobile": "Tesco Mobile's media coverage focused solely on the brand value of 'Value' (100%). This was driven by Ofcom's report, which highlighted that Tesco Mobile attracted the fewest complaints for mobile services. This commendable performance underscores Tesco Mobile's commitment to offering high-quality, reliable services to its customers.",
                "Virgin Mobile": "Virgin Mobile did not receive any positive brand value mentions in the observed media coverage. The analysed publications and stories only associate the brand with negative sentiment due to price increases, discontinuation of services, and a high volume of complaints reported by Ofcom.",
                "Vodafone": "Vodafone's media coverage predominantly highlighted its Innovation, with 29% of brand values linked to the proposed merger with Three UK and its partnership with Samsung for Open RAN expansion. A focus on Transparency/Trust and Value (both at 14%) also emerged, with Vodafone's communication regarding the 5G signal and cost-effective data plans. Inclusivity (5%) was spotlighted in their involvement with The National Databank to combat data poverty. Key mentions were driven by their impending merger and partnerships, affordability, and innovative steps.",
                "Voxi": "The media coverage of Voxi, a brand of Vodafone, didn't explicitly link to any positive brand values such as design, innovation, inclusivity, sustainability, transparency/trust, or value. Mentions were neutral, with references primarily arising from discussions about the proposed merger between Vodafone and Three UK. The brand was presented in the context of potential adjustments to its strategy following the merger."
            }

            dict_brand_neg_values_text = {
                "Disney": "Placeholder text. Add dynamic text or use GPT to generate.",
                "Three": "Three's media coverage predominantly reflected negative brand values of Transparency/Trust (15%) and Value (10%). The brand's lack of Transparency/Trust was noted in reports like Yahoo! UK and Ireland, Sussex Express, and Basildon Echo, where Three's proposed 5G mast installations sparked community backlash. Trust issues were amplified by perceived health risks and inappropriate mast locations. Negative sentiments around Value were driven by reports of price increases (Caithness Business Index, Times of Bristol) and high complaint rates (Ofcom). Despite the minor reference to Design (3%), it added to the negativity, as in The Daily Telegraph where Three's mast threatened to disrupt the historical skyline.",
                "BT Mobile": "The negative media coverage for BT Mobile was primarily related to the brand value of 'Value'. The brand received criticism due to high complaint rates for its mobile services, as reported by Ofcom. This suggests that customers were dissatisfied with the value they received from BT Mobile's services, which significantly influenced the perception of the brand in a negative way.",
                "EE": "EE's media coverage was negatively impacted by issues related to 'Value' and 'Transparency/Trust'. Publications including the Daily Express and the Caithness Business Index reported on customer discontent due to a significant increase in prices for EE's services. This was perceived as a lack of value for money, while the sudden price hike also raised questions about EE's transparency and trustworthiness. The rising prices led to dissatisfaction, suggesting that customers might look elsewhere for better value.",
                "O2": "In the media, O2 was negatively portrayed in relation to the 'Value' aspect of their brand. This was primarily driven by upcoming broadband price increases, as reported by the Caithness Business Index and Telecoms News From NTSI. These hikes, reaching up to 17% as per the reports, sparked customer dissatisfaction and cast O2 in a negative light, as consumers started looking for better value elsewhere.",
                "Sky Mobile": "Sky Mobile had no negative brand values distributed in its media coverage. The mention in Times of Bristol was rather positive, highlighting a £5 discount on a new data plan, indicating good value to customers. Therefore, no negative values were associated with Sky Mobile's coverage during this period.",
                "Smarty": "There were no negative brand values associated with Smarty in the analyzed media coverage. The articles primarily reported on Smarty's new social tariff, its position in the potential Three UK and Vodafone merger, and its data deal offering double the usual data for the same price. These mentions are positive or neutral, suggesting a positive public perception of the brand during this period.",
                "Tesco Mobile": "There were no negative brand values associated with Tesco Mobile in the media coverage analyzed. In the noted article from Ofcom, the brand was positively recognized for having the fewest complaints among mobile services, reflecting a high customer satisfaction level during this period.",
                "Virgin Mobile": "Negative media coverage for Virgin Mobile centered around 'Value' and 'Transparency/Trust' with prominent mentions of price hikes and discontinuation of a popular service. These issues were spotlighted in articles by the Times of Bristol and Daily Express, resulting in a negative sentiment. The Ofcom article also negatively emphasized Virgin Mobile due to high complaint rates for its services.",
                "Vodafone": "Negative media coverage for Vodafone predominantly related to 'Value', driven by mentions of significant price increases and high complaint rates. Headlines from Investing.com UK, The Times, and Caithness Business Index spotlighted price hikes, casting a negative sentiment, while an Ofcom report linked Vodafone to leading broadband and mobile service complaints. Telecoms News From NTSI hinted at customer dissatisfaction due to price hikes.",
                "Voxi": "Negative brand values were not highlighted in the media coverage for Voxi. The brand, being a subsidiary of Vodafone, was neutrally mentioned in context with the imminent Vodafone and Three UK merger in ISPreview and Mobile Europe, without any negative implications related to design, innovation, inclusivity, sustainability, transparency/trust, or value."
            }

            # %% GENERATE PPT +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #  CREATE THE PPT FILE -----------------------------------------------------
            ppt = Presentation()
            ppt.slide_width, ppt.slide_height = Inches(13.33), Inches(7.5)
            blank_slide_layout = ppt.slide_layouts[6] # to create blank slide template, use 6 as an argument for slide_layouts
            slide_number = 0 # slide number, set to zero to be incremented by 1 with each new slide

            # CREATE TITLE SLIDE ------------------------------------------------------
            create_slide_front (ppt, blank_slide_layout, company, month_text)
            
            # CREATE LEADING AUTHORS SLIDE --------------------------------------------
            create_slide_authors(df, ppt, blank_slide_layout, company, company_short, company_color,
                        top_author_by_vol, top_author_by_vol_surname, top_author_by_vol_source, top_author_vol, list_top_authors, list_top_authors_vols)
            
            # CREATE LEADING SOURCES SLIDE --------------------------------------------
            create_slide_sources(df, ppt, blank_slide_layout, company, company_short, company_color,
                        top_source_by_vol, top_source_vol, top_source_top_author, top_source_top_author_vol, 
                        list_top_sources_by_vol, list_top_sources_vol)
            
            # CREATE METRIC SLIDES --------------------------------------------
            for brand_present in brands_present:
                create_slide_sentiment(ppt, blank_slide_layout, brand_present, dict_brand_sentiment, dict_brand_sent_text, company_color_yn, company_logo_yn)
                create_slide_prominence(ppt, blank_slide_layout, brand_present, dict_brand_prominence, dict_brand_prom_text, company_color_yn, company_logo_yn)
                create_slide_corp_con(ppt, blank_slide_layout, brand_present, dict_brand_corp_con, dict_brand_corp_con_text, company_color_yn, company_logo_yn)
                create_slide_topics(ppt, blank_slide_layout, brand_present, dict_brand_topics, dict_brand_topics_text, company_color_yn, company_logo_yn)
                """
                # Spokespeople slide temporarily disabled until bugs ironed out
                create_slide_spokespeople(ppt, blank_slide_layout, brand_present, dict_brand_spokespeople, dict_brand_spokespeople_text, company_color_yn, company_logo_yn)
                """
                create_slide_pos_values(ppt, blank_slide_layout, brand_present, dict_brand_pos_values, dict_brand_pos_values_text, company_color_yn, company_logo_yn)
                create_slide_neg_values(ppt, blank_slide_layout, brand_present, dict_brand_neg_values, dict_brand_neg_values_text, company_color_yn, company_logo_yn)
            """

            # CREATE CORPORATE/CONSUMER SLIDES ------------------------------
            # Create a corporate/consumer slide for each brand based on the create_slide_corp_con function, defined in func_create_slides.py
            # Slides will be created in the order set by brands_present
            # This order has been defined earlier in the script and should put company (client) first, and competitors (other brands) subsequently in AZ order
            for brand_present in brands_present:
                create_slide_corp_con(ppt, blank_slide_layout, brand_present, dict_brand_corp_con, dict_brand_corp_con_text, company_color_yn, company_logo_yn)

            # CREATE BRAND SENTIMENT SLIDES ---------------------------------
            # Identical to brand corporate/consumer slides above, but for prominence
            for brand_present in brands_present:
                create_slide_sentiment(ppt, blank_slide_layout, brand_present, dict_brand_sentiment, dict_brand_sent_text, company_color_yn, company_logo_yn)

            # CREATE BRAND PROMINENCE SLIDES ---------------------------------
            # Identical to brand sentiment slides above, but for prominence
            for brand_present in brands_present:
                create_slide_prominence(ppt, blank_slide_layout, brand_present, dict_brand_prominence, dict_brand_prom_text, company_color_yn, company_logo_yn)

                """

            # %% SAVE POWERPOINT FILE TO UPLOAD FOLDER ------------------------
            dt_string = str(datetime.now().strftime("%Y-%m-%d, %H-%M-%S")) # get current time and format it
            ppt_filename = f'Onclusive_{company}_{month_text}_{year} - ({dt_string}).pptx'
            ppt_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'PPT_Outputs', ppt_filename)
            ppt.save(ppt_file_path)
            print(f'\nAll processes complete. Please check the folder for your presentation. It will appear in the folder {ppt_file_path}')    

            return jsonify({'filename': ppt_filename})   



# %% if name main
# Ensures that script only runs if directly executed (rather than called from another script)
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'outputs'  # Set the upload folder
    app.run(debug=True)