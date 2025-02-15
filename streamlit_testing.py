# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 00:29:35 2025

@author: Carson
"""

import streamlit as st
import numpy as np
import pandas as pd


#TABLE WITH MAX VALUES IN EACH COLUMN HIGHLIGHTED
# =============================================================================
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
# 
# st.dataframe(dataframe.style.highlight_max(axis=0))
# =============================================================================

#MAP Example
# =============================================================================
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])
# 
# st.map(map_data)
# =============================================================================

#SLIDER FUNCTION EXAMPLE -> slide value is input into function
# =============================================================================
# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
# =============================================================================



#CHECK BOXES TO SHOW HIDE DATA
# =============================================================================
# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c'])
# 
#     chart_data
# =============================================================================

#SELECT BOXES
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
