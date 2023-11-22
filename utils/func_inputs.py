# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:30:22 2022

@author: rober
"""

# %% input checker ------------------------------------------------------------

from utils.dicts_data_to_ppt import dict_allowed_inputs

def input_checker(input_value, var_name):
    good_vals = ', '.join(dict_allowed_inputs[var_name])
    while input_value not in dict_allowed_inputs[var_name]:
        input_value = input(f'Input for {var_name} does not match expected formatting. '
                           f'Please enter from list of allowed values '
                           f'({good_vals}) : ')
    
    # return input value and list of months from prompt if looking at month select, otherwise return only input value
    if var_name == 'month_select' and input_value in ['Y', 'y']: # take list of months if user answers Y to month selection
        list_months = [int(i) for i in input('Please enter a comma separated list of months, in number format\n'
                    'e.g. 1,2,5,12 to include Jan, Feb, May and Dec: ').split(',')]
        return input_value, list_months
    elif var_name == 'month_select' and input_value in ['N', 'n']:
        list_months = [1,2,3,4,5,6,7,8,9,10,11,12]
        return input_value, list_months
    else:
        return input_value
    