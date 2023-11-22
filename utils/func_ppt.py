# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 18:22:30 2022

@author: rober
"""

from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement

# PPT-specific functions ------------------------------------------------

# %% set reverse categories on axis -------------------------------------------

# function that replicates the "Categories in Reverse Order" UI option in PPT
# not currently available by default in the pptx library
def set_reverse_categories(axis):
    ele = axis._element.xpath(r'c:scaling/c:orientation')[0]
    ele.set("val", "maxMin")
    
# %% define subelement for setting cell borders -------------------------------
    
def SubElement(parent, tagname, **kwargs):
    element = OxmlElement(tagname)
    element.attrib.update(kwargs)
    parent.append(element)
    return element

# %% set cell borders ---------------------------------------------------------

def set_cell_border(cell, border_color="000000", border_width='12700'):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for lines in ['a:lnL','a:lnR','a:lnT','a:lnB']:
        ln = SubElement(tcPr, lines, w=border_width, cap='flat', cmpd='sng', algn='ctr')
        solidFill = SubElement(ln, 'a:solidFill')
        srgbClr = SubElement(solidFill, 'a:srgbClr', val=border_color)
        prstDash = SubElement(ln, 'a:prstDash', val='solid')
        round_ = SubElement(ln, 'a:round')
        headEnd = SubElement(ln, 'a:headEnd', type='none', w='med', len='med')
        tailEnd = SubElement(ln, 'a:tailEnd', type='none', w='med', len='med')


