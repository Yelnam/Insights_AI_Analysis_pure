# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:54:01 2022

@author: rober
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.enum.chart import XL_TICK_MARK
from utils.func_ppt import set_reverse_categories

# %%  apply data labels -------------------------------------------------------

def apply_data_labels(plot,
                      has_labels = True,
                      pos = XL_LABEL_POSITION.ABOVE,
                      font = 'Calibri',
                      fontsize = 9,
                      color = RGBColor(0,0,0),
                      numformat = '#,##0',
                      bold = False,
                      rotate = False):
    plot.has_data_labels = has_labels
    data_labels = plot.data_labels
    data_labels.position = pos
    data_labels.font.name = font
    data_labels.font.size = Pt(fontsize)
    data_labels.font.color.rgb = color
    data_labels.number_format = numformat
    data_labels.font.bold = bold
    if rotate == True:
        data_labels._element.get_or_add_txPr().bodyPr.set('rot','-5400000')
        
# %%  format y axis -----------------------------------------------------------
        
def format_y_axis (chart,
                   data_series,
                   visible = True,
                   major_unit = 0,
                   major_grid = True,
                   major_grid_color = RGBColor(0,0,0),
                   minor_grid = False,
                   line_width = Inches(0),
                   line_color = RGBColor(0,0,0),
                   label_size = 9,
                   label_color = RGBColor(0,0,0),
                   label_font = 'Calibri',
                   axis_max = 0,
                   axis_min = 0,
                   tick_mark = XL_TICK_MARK.NONE):
    yAxis = chart.value_axis
    yAxis.visible = visible
    yAxis.has_major_gridlines = major_grid
    yAxis.has_minor_gridlines = minor_grid
    yAxis.major_gridlines.format.line.color.rgb = major_grid_color
    yAxis.format.line.width = line_width
    yAxis.format.line.color.rgb = line_color
    yAxis.tick_labels.font.size = Pt(label_size)
    yAxis.tick_labels.font.color.rgb = label_color
    yAxis.tick_labels.font.name = label_font
    yAxis.minimum_scale = 0
    yAxis.major_tick_mark = tick_mark
        
    
    # set y axis height 50% above max of all volumes

    chart_max_y = max(data_series) * 1.5
    # round to nearest 100 (if larger than 500)
    if chart_max_y > 500:
        chart_max_y = int(round(chart_max_y/10, -1) * 10)
    else:
        pass
    
    if axis_max != 0: # if axis max has been set manually through args
        yAxis.maximum_scale = axis_max # use manual setting
    else:
        yAxis.maximum_scale = chart_max_y # otherwise use calculation
    
    if major_unit != 0: # if axis max has been set manually through args    
        yAxis.major_unit = major_unit
    else:
        yAxis.major_unit = chart_max_y/5 # otherwise use 1/5 axis max
        
    return chart_max_y

# %%  format y axis for bar chart ---------------------------------------------

def format_y_axis_bar (chart,
                   visible = True,
                   major_unit = 0,
                   major_grid_color = RGBColor(0,0,0),
                   major_grid = False,
                   minor_grid = False,
                   line_width = Inches(0),
                   line_color = RGBColor(0,0,0),
                   label_size = 9,
                   label_color = RGBColor(0,0,0),
                   label_font = 'Calibri',
                   axis_max = 0,
                   axis_min = 0,
                   tick_mark = XL_TICK_MARK.NONE):
    yAxis = chart.category_axis
    yAxis.visible = visible
    yAxis.major_gridlines.format.line.color.rgb = major_grid_color
    yAxis.has_major_gridlines = major_grid
    yAxis.has_minor_gridlines = minor_grid
    yAxis.format.line.width = line_width
    yAxis.format.line.color.rgb = line_color
    yAxis.tick_labels.font.size = Pt(label_size)
    yAxis.tick_labels.font.color.rgb = label_color
    yAxis.tick_labels.font.name = label_font
    yAxis.minimum_scale = 0
    yAxis.major_tick_mark = tick_mark