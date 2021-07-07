# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:40:01 2021

@author: richard chai
https://www.linkedin.com/in/richardchai/

"""

import streamlit as st
st.set_page_config('RSI Chart', page_icon=':shark:',layout='centered')

#import numpy as np
import pandas as pd
import datetime as dt

#import plotly.graph_objects as go
#from plotly.subplots import make_subplots

from rsi_LoadData import loadStkData
from rsi_Calc import RSI_Calc
from plot_Plotly import plotly_Plot_RSA

tickers = sorted(["FB", "AAPL", "AMZN", "IBM", "GOOGL", "MSFT","TSLA"])
OHLC = ['Open','High','Low','Close','Adj Close','Volume']
#startDate = dt.date(2015,1,1)
startDate = dt.datetime.now() - dt.timedelta(days=5*365)  # 5 years ago
# endDate = dt.date(2015,12,31)
endDate = dt.date.today()
RSI_Mthd = ['SMA','EWA']
window = 14

# source,tickers, startDate, endDate, interval='1d', apiKey=None
@st.cache
def loadData(src,tickers,startDtd, endDtd, interval='1d', apiKey=None):    
    return loadStkData(src,tickers,startDtd,endDtd,interval,apiKey)

# Left:  1 side bar, submit using form
# Right: 3 horizontal containers, stack on top of each other

with st.form(key='frmChartOpts'):
    with st.sidebar:
        st.subheader('Chart Options')
        selTicker = st.selectbox('TICKER',tickers,index=0)
        selOHLC = st.selectbox('OHLC', OHLC,index=4)
        selDateStart = st.date_input('Start Date (yy/mm/dd)',startDate,startDate,endDate)
        selDateEnd = st.date_input('End Date (yy/mm/dd)',endDate,startDate,endDate)
        selRSIMthd = st.radio('RSI Method',RSI_Mthd)
        selWindow = st.slider('Sliding Window',5,20,14)
        btnSubmit = st.form_submit_button(label='Generate Chart')

cHeader = st.beta_container()
cContent = st.beta_container()
cFooter = st.beta_container()

with cHeader:
    st.header('RSI Charts')
    st.subheader('Selected stocks - 5 years ago until now.')

with cContent:
    # load stock data      
    df_Loaded = loadData('yFinance', tickers,startDate,endDate)
    df = df_Loaded.copy()  # make a copy to avoid a cache miss  
        
    # # df_T = df[ticker][chart_Date_Start:chart_Date_End].copy()
    
    # 1st, get the columns for the selected ticker ONLY            
    df_T = df.iloc[:,df.columns.get_level_values(0)==selTicker]
    # because df is a 2 level (multiindex) column, the next code line
    # retrieves level==1 columns i.e. (OHLC), because RSI_Calc expects
    # to receive a 1 level column df
    df_T = df_T[selTicker][selDateStart:selDateEnd]
    
    df_T = RSI_Calc(df_T, selOHLC, method=selRSIMthd, window=selWindow)
    
    # make the next line a cache?
    fig = plotly_Plot_RSA(selTicker,df_T, selOHLC,
                    'RSI_'+selRSIMthd+'_'+selOHLC,
                    RSA_Mthd=selRSIMthd, overSoldTres=20, overBoughtTres=80)   
    
    st.plotly_chart(fig)
    
    if st.checkbox('Show dataframe'):        
        st.write(f'Selected Ticker: {selTicker}')
        st.write(df_T)    

with cFooter:
    #st.subheader('Contact')
    expander = st.beta_expander('Contact',expanded=True)
    expander.write('- Richard Chai https://www.linkedin.com/in/richardchai/')
    
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
#         width: 220px;
#     }
#     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
#         width: 220px;
#         margin-left: -500px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



