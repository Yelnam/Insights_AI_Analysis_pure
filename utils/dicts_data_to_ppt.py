# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 17:11:44 2022

@author: rober
"""

from pptx.dml.color import RGBColor
from pptx.util import Inches

# %% company headline exclusion -----------------------------------------------

# add terms you do not want to appear in headlines by company inside the []
# put each term in single quotes and separate terms with a comma
dict_hl_exclusion = {
    'abrdn':[],
    'ADNOC':[],
    'Aston Martin':[],
    'BNP Paribas Real Estate':[],
    'Born Free Foundation':[],
    'Bupa':[],
    'Burness Paull LLP':[],
    'Continental Tyres':['League Cup', 'Continental Cup', 'Women\'s Continental'],
    'Cygnet Health Care':[],
    'Dechert LLP':[],
    'ghd':[],
    'Guardian News and Media':[],
    'KFC':['Australia', 'Australian', 'australia', 'australian', 'SAVERS'],
    'Lloyds Banking Group':[],
    'Mundipharma':[],
    'NHS Education for Scotland':[],
    'Royal College of General Practitioners':[],
    'Shangri-La - Core Markets':[],
    'Shangri-La - US':[],
    'The Health Foundation':[],
    'Three':[],
    'Unite':[]
    }



# %% company names ------------------------------------------------------------

# provides variations on the name entered by the user for use in diff places
# uses full 2021 list as of 2022 12 14, with KFC and LBG added as of 2022 12 21
dict_company_names = { # in order: title, full, short, image, headline, alt
    'abrdn':['abrdn','abrdn','abrdn','abrdn','abrdn','abrdn'],
    'ADNOC':['ADNOC', 'Abu Dhabi National Oil Company', 'ADNOC', 'ADNOC', 'Abu Dhabi National Oil Company', 'ADNOC'],
    'Aston Martin': ['Aston Martin','Aston Martin','Aston Martin','Aston Martin','Aston Martin','Aston Martin'],
    'BNP Paribas Real Estate':['BNP Paribas Real Estate','BNP Paribas Real Estate','BNP','BNP Paribas Real Estate','BNP Paribas Real Estate','BNP'],
    'Born Free Foundation':['Born Free Foundation','Born Free Foundation','Born Free','Born Free Foundation','Born Free Foundation','Born Free '],
    'BT Enterprise':['BT Enterprise','BT Enterprise','BT Enterprise','BT Enterprise','BT Enterprise','BT Enterprise'],
    'Bupa':['Bupa','Bupa','Bupa','Bupa','Bupa','Bupa'],
    'Burness Paull LLP':['Burness Paull LLP','Burness Paull LLP','Burness Paull','Burness Paull LLP','Burness Paull LLP','Burness Paull LLP'],
    'Continental Tyres':['Continental Tyres','Continental Tyres','Continental','Continental Tyres','Continental Tyres','Continental'],
    'Countrywide':['Countrywide','Countrywide','Countrywide','Countrywide','Countrywide','Countrywide'],
    'Cygnet Health Care':['Cygnet Health Care','Cygnet Health Care','Cygnet','Cygnet Health Care','Cygnet Health Care','Cygnet'],
    'Dechert LLP':['Dechert LLP','Dechert LLP','Dechert','Dechert LLP','Dechert LLP','Dechert'],
    'Disney':['Disney','Disney','Disney','Disney','Disney','Disney'],
    'ghd':['ghd','ghd','ghd','ghd','ghd','good hair day'],
    'Guardian News and Media':['Guardian News and Media','Guardian News and Media','Guardian','Guardian News and Media','Guardian','Guardian'],
    'John Lewis & Partners':['John Lewis & Partners','John Lewis & Partners','John Lewis','John Lewis & Partners','John Lewis & Partners','John Lewis'],
    'KFC':['KFC','Kentucky Fried Chicken','KFC','KFC','KFC','Kentucky Fried Chicken'],
    'Lawn Tennis Association':['Lawn Tennis Association','Lawn Tennis Association','LTA','Lawn Tennis Association','Lawn Tennis Association','LTA'],
    'Lloyds Banking Group':['Lloyds Banking Group', 'Lloyds Banking Group', 'LBG', 'Lloyds Banking Group', 'Lloyds Banking Group', 'LBG'],
    'Mundipharma':['Mundipharma','Mundipharma','Mundipharma','Mundipharma','Mundipharma','Mundipharma'],
    'Nestle':['Nestlé','Nestlé','Nestlé','Nestlé','Nestlé','Nestle'],
    'NHS Digital':['NHS Digital','NHS Digital','NHS Digital','NHS Digital','NHS Digital','NHS Digital'],
    'NHS Education for Scotland':['NHS Education for Scotland','NHS Education for Scotland','NHS EfS','NHS Education for Scotland','NHS Education for Scotland','NHS'],
    'NHS Wirral University Teaching Hospital ':['NHS Wirral University Teaching Hospital ','NHS Wirral University Teaching Hospital ','NHS WUTH','NHS Wirral University Teaching Hospital ','NHS Wirral','NHS'],
    'Pool Reinsurance Company':['Pool Reinsurance Company','Pool Reinsurance Company','Pool Re','Pool Reinsurance Company','Pool Reinsurance Company','Pool Re'],
    'Royal College of General Practitioners':['Royal College of General Practitioners','Royal College of General Practitioners','RCGP','Royal College of General Practitioners','Royal College of General Practitioners','Royal College'],
    'Shangri-La - Core Markets':['Shangri-La - Core Markets','Shangri-La','Shangri-La','Shangri-La','Shangri-La','Shangri'],
    'Shangri-La - US':['Shangri-La - US','Shangri-La','Shangri-La','Shangri-La','Shangri-La','Shangri'],
    'Strutt & Parker':['Strutt & Parker','Strutt & Parker','Strutt & Parker','Strutt & Parker','Strutt & Parker','Strutt & Parker'],
    'Sussex Police':['Sussex Police','Sussex Police','Sussex Police','Sussex Police','Sussex Police','Sussex Police'],
    'The Health Foundation':['The Health Foundation','The Health Foundation','Health Foundation','The Health Foundation','Health Foundation','Health Foundation'],
    'Three':['Three','Three','Three','Three','Three','Three'],
    'Unilever':['Unilever','Unilever','Unilever','Unilever','Unilever','Unilever'],
    'Unite':['Unite the Union','Unite the Union','Unite','Unite','Unite','Unite']
    }

# %% company logos ------------------------------------------------------------

# dictionary of positions and sizes for logos (files stored in Images/Logos)
dict_company_logos = { # left, top, width, height
    'abrdn':[12.01, 0.35, 0.91, 0.57],
    'ADNOC':[],
    'Aston Martin':[], # empty lists indicate logo not yet added
    'BNP Paribas Real Estate':[12.38, 0.35, 0.54, 0.54],
    'Born Free Foundation':[11.5, 0.36, 1.46, 0.51],
    'BT Mobile': [12.33, 0.22, 0.77, 0.77],
    'Bupa':[12.45, 0.3, 0.57, 0.57],
    'Burness Paull LLP':[11.24, 0.33, 1.74, 0.44],
    'Continental Tyres':[11.58, 0.37, 1.38, 0.29],
    'Cygnet Health Care':[12.03, 0.32, 0.91, 0.47],
    'Dechert LLP':[11.79, 0.34, 1.15, 0.39],
    'Disney':[12.05, 0.17, 1.01, 1.04],
    'EE':[12.54, 0.18, 0.85, 0.49],
    'ghd':[],
    'Guardian News and Media':[12.08, 0.27, 0.89, 0.59],
    'KFC':[],
    'Lloyds Banking Group':[],
    'Mundipharma':[12.01, 0.25, 1.02, 0.56],
    'NHS Education for Scotland':[12.43, 0.26, 0.6, 0.6],
    'O2':[12.28, 0.26, 0.68, 0.69],
    'Royal College of General Practitioners':[11.4, 0.28, 1.59, 0.53],
    'Shangri-La - Core Markets':[11.8, 0.25, 1.16, 0.58],
    'Shangri-La - US':[11.8, 0.25, 1.16, 0.58],
    'Sky Mobile': [11.41, 0.19, 0.82, 1.64],
    'Smarty': [11.45, 0.28, 0.66, 1.61],
    'Tesco Mobile': [11.4, 0.34, 0.57, 1.55],      
    'The Health Foundation':[11.55, 0.28, 1.4, 0.45],
    'Three':[12.46, 0.19, 0.85, 0.6],
    'Unite':[12.42, 0.25, 0.69, 0.55],
    'Virgin Mobile':[12.08, 0.21, 0.8, 0.94],
    'Vodafone':[12.01, 0.23, 0.74, 1.03],
    'Voxi': [12.31, 0.22, 0.79, 0.8]
    }

# %% company colors -----------------------------------------------------------

dict_company_colors = { # use hex colors
    'abrdn': '000000',
    'ADNOC':'1A4F92', 
    'Aston Martin': '00A58A',
    'BNP Paribas Real Estate': '158152',
    'Born Free Foundation': '0A0A0A',
    'BT Mobile': '5514B4',
    'Bupa': '4D6EC5',
    'Burness Paull LLP': '412E5F',
    'Continental Tyres': 'E6AB35',
    'Cygnet Health Care': '005A94',
    'Dechert LLP': '00395C',
    'Disney': '4562B0',
    'EE': '1D9F9E',
    'ghd':'C9B36C',
    'Guardian News and Media': '162884',
    'KFC':'F40022',
    'Lloyds Banking Group':'00864F',
    'Mundipharma': '006BB6',
    'NHS Education for Scotland': '06A1E5',
    'O2': '0112AA',
    'Royal College of General Practitioners': '18295B',
    'Shangri-La - Core Markets': 'CDA62D',
    'Shangri-La - US': 'CDA62D',
    'Sky Mobile': 'FF3E5E',
    'Smarty': '434449',
    'Tesco Mobile': '0152A1',
    'The Health Foundation': 'B91E37',
    'Three': 'FF7C68',
    'Unite': 'E2231A',
    'Virgin Mobile': 'ED1736',
    'Vodafone': 'E60000',
    'Voxi': '181714'
    }

# %% media colors -------------------------------------------------------------

dict_media_colors = { # use hex colors
    'media_1': '162746',
    'media_2': '264378',
    'media_3': '4674C6',
    'media_4': '87A6D9',
    'media_5': 'B0C3E6',
    'media_other': '45D36A',
    }

# %% month to text ------------------------------------------------------------
    
# for getting text values from the report month integer input
# used in report name, front page (& elsewhere if required)
dict_month_to_text = {
    1:['Jan','January','31'], 
    2:['Feb','February','28'], 
    3:['Mar','March','31'], 
    4:['Apr','April','30'], 
    5:['May','May','31'], 
    6:['Jun','June','30'], 
    7:['Jul','July','31'], 
    8:['Aug','August','31'], 
    9:['Sep','September','30'], 
    10:['Oct','October','31'], 
    11:['Nov','November','30'], 
    12:['Dec','December','31']
    }

# %% low numbers --------------------------------------------------------------

# used to substitute text in commentary if value below ten
dict_low_numbers = {
    0:'zero',
    1:'one', 
    2:'two', 
    3:'three', 
    4:'four', 
    5:'five', 
    6:'six', 
    7:'seven', 
    8:'eight', 
    9:'nine', 
    }

# %% allowed inputs -----------------------------------------------------------

# for determining expected inputs 
dict_allowed_inputs = {
    'year': ['2021', '2022', '2023'],
    'del_or_pub': ['P', 'p', 'D', 'd'],
    'month_select': ['Y', 'y', 'N', 'n'],
    'company_color_yn': ['Y', 'y', 'N', 'n'],
    'company_logo_yn': ['Y', 'y', 'N', 'n']
    }