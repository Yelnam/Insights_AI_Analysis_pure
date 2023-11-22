# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 18:35:31 2022

@author: rober
"""

# %% rounder ------------------------------------------------------------------

def rounder(input_number):
    input_number_text = (f'{round(input_number/1000000000,1)}bn' if input_number >= 1000000000 
                      else 
                      f'{round(input_number/1000000,1)}m' if input_number >= 1000000 
                      else 
                      f'{str(input_number)[:-3]},{str(input_number)[-3:]}' if input_number >= 1000
                      else
                      f'{input_number}')
    return input_number_text

# %% rounder long -------------------------------------------------------------

def rounder_long(input_number):
    input_number_text = (f'{round(input_number/1000000000,1)} billion' if input_number >= 1000000000 
                      else 
                      f'{round(input_number/1000000,1)} million' if input_number >= 1000000 
                      else 
                      f'{str(input_number)[:-3]},{str(input_number)[-3:]}' if input_number >= 1000
                      else
                      f'{input_number}')
    return input_number_text