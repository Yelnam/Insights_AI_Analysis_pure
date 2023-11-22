# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:18:16 2022

@author: rober
"""

import pandas as pd
from utils.dicts_data_to_ppt import dict_company_names, dict_hl_exclusion

df_temp = pd.DataFrame()

# %% generate headlines -------------------------------------------------------

def generate_headlines(df, comp, co_hl, co_alt):
    try:
        # filter for company headline or alt names (expected headline formats)
        df_client_HLs = df[df['Headline'].str.contains(co_hl) | df['Headline'].str.contains(co_alt)]
        
        # remove broadcast, as headlines will not be usable
        df_client_HLs= df_client_HLs[~df_client_HLs['Media'].str.contains('Broadcast')]
        
        # filter out unwanted phrases
        df_client_HLs = df_client_HLs[
            [not any(ele in df_client_HLs['Headline'].iloc[i]
                 for ele in dict_hl_exclusion[comp]) 
             for i in range(len(df_client_HLs))]
            ]
        
        # only take headlines bigger than company alt (at least an additional word) - otherwise you get HLs which are just the company name
        #     alt used as generally shorter, longer names prohibitive
        df_client_HLs = df_client_HLs[df_client_HLs['Headline'].str.len() > len(co_hl) + 10]
        
        # but shorter than 100 characters
        #     (this step skipped for RGCPs, name length means HLs always longer
        #      RGCPs will required manual cleaning on PPT
        if comp != 'Royal College of General Practitioners':
            df_client_HLs = df_client_HLs[df_client_HLs['Headline'].str.len() < 100]
        else:
            pass
        
        # put escape character before apostrophes to get properly formatted outputs
        df['Headline'] = [i.replace("'","\'") for i in df['Headline']]
        
        # get top pubs by reach which include relevant HLs
        df_client_HLs_top_pubs_reach = (df_client_HLs
                                               .groupby('Publication', as_index=False)
                                               ['Reach'].mean()
                                               .sort_values('Reach', ascending=False)
                                               )
        
        # list the sources, remove online ecoverage
        list_client_HL_sources = [i for i in df_client_HLs_top_pubs_reach['Publication'] if i != 'Online eCoverage (Web)']
        
        # list the HLs (takes first HL in df filtered by each top HL source at a time)
        list_client_HLs = [df_client_HLs['Headline'][df_client_HLs['Publication'] == i]
                           .iloc[0] for i in list_client_HL_sources]
        
        hl1, hl1_source = list_client_HLs[0], list_client_HL_sources[0]
        hl2, hl2_source = list_client_HLs[1], list_client_HL_sources[1]
        hl3, hl3_source = list_client_HLs[2], list_client_HL_sources[2]
        hl4, hl4_source = list_client_HLs[3], list_client_HL_sources[3]
        
        return hl1, hl1_source, hl2, hl2_source, hl3, hl3_source, hl4, hl4_source
    
    except:
        hl1, hl1_source = 'Error generating headlines', 'Please get headlines manually'
        hl2, hl2_source = 'Error generating headlines', 'Please get headlines manually'
        hl3, hl3_source = 'Error generating headlines', 'Please get headlines manually'
        hl4, hl4_source = 'Error generating headlines', 'Please get headlines manually'
        
        return hl1, hl1_source, hl2, hl2_source, hl3, hl3_source, hl4, hl4_source