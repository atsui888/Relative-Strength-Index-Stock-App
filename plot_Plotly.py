# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:34:52 2021

@author: richard chai
https://www.linkedin.com/in/richardchai/
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from plotly import tools
# import plotly.offline as py
# import plotly.express as px

import streamlit as st

@st.cache
def plotly_Plot_RSA(ticker, df, OHLC_ColName, RSIColName, height=680,width=800, RSA_Mthd='SMA', overSoldTres=20, overBoughtTres=80):
    '''
    Creates and Displays a RSA Plot using plotly
    For oversold and overbought texts to appear, set argument RSA_Mtd=='SMA'
    The dataframe index should be in datetime, although it will still be plotted otherwise.
    
        Parameters
            ticker (str)          : The Stock Ticker Symbol for the chart title
            df (pandas dataframe) : The dataframe containing the data to be charted
            OHLC_ColName (str)    : The column name containing y-axis data for chart 1
            RSIColName (str)      : The column name containing  y-axis data for chart 2 (RSI)
                                    It could be the col calculated with SMA or the col calcuated
                                    with EWA.
            height (int)          : desired pixel height of chart
            width (int)           : desired pixel width of chart
            RSA_Mthd (str)        : Currently only 2 choices {SMA | EWM}, default is 'SMA'
            overSoldTres (int)    : When RSI < this treshold, a text appears in the chart 'oversold'
            overBoughtTres (int)  : When RSI > this treshold, a text appears in the chart 'overbought'
        
        Return:
            None
    '''
    
    fig = make_subplots(rows=2, cols=1,vertical_spacing=0.13,
                   subplot_titles=(OHLC_ColName, "RSI Values"),
                   column_widths=[1.0], row_heights=[0.5,0.5])

    fig.append_trace(go.Scatter(
        x=df.index,
        y=df[OHLC_ColName],
        mode='lines',
        #name='Adj Close ($)'  # default name is 'trace 0'
        name = OHLC_ColName
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=df.index,
        y=df[RSIColName],
        line_color="forestgreen",
        line_width=1,
        mode='lines+markers',
        #mode='lines',
        name='RSI Value'
    ), row=2, col=1)


    if RSA_Mthd == 'SMA':
        fig.add_hline(y=20, annotation_text="RSI = 20", annotation_position="bottom right",
              line_width=2, line_dash="dash", line_color="red", row=2,col=1)
        fig.add_hline(y=80, annotation_text="RSI = 80", annotation_position="bottom right",
               line_width=2, line_dash="dash", line_color="red", row=2,col=1)

        for i, row in df.iterrows():
            if row[RSIColName] < overSoldTres:
                fig.add_annotation(x=i, y=row[RSIColName],text="OverSold",
                                   font=dict(color="#ff0000"), opacity=0.8, ax=-34,ay=24,
                                   showarrow=True,arrowhead=1, arrowcolor="#FF0000", row=2,col=1) 
            if row[RSIColName] > overBoughtTres:
                fig.add_annotation(x=i, y=row[RSIColName],text="OverBought",
                                   font=dict(color="#ff0000"), opacity=0.8, ax=-34,ay=-24,
                                   showarrow=True,arrowhead=1,arrowcolor="#FF0000", row=2,col=1) 
        
    fig.update_layout(
        title_text= f'Stock Ticker: {ticker} from {df.index[0].date()} to {df.index[-1].date()}',        
        template='simple_white', height=height) 
        # height=height, width=width, autosize=True
    
    # fig.show()
    return fig   