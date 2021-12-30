# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:18:05 2021

@author: richard chai
https://www.linkedin.com/in/richardchai/
"""

import pandas as pd
import math
import streamlit as st

@st.cache
def RSI_Calc(df_OHLC, colName, method="SMA", window = 14):
    '''
    Returns the OHLC dataframe with a new column containing RSI numbers.
    
    RSI can be calculated on not just the 'Close' but also 'Adjusted Close' and as an "oscillating 
    reversion to the mean" indicator, it can be used for more than just financial stocks. Use 
    'colName' to indicate which column is to be used for the calculations.
    
    e.g. 
            df_RSI = RSI(data, 'Adj Close', method='SMA')
            df_RSI = RSI(data, 'Adj Close', method="EWA")
    

            Parameters:
                df_OHLC (pandas dataframe) : containing the data which RSI is to be calculated
                colName (str)              : name of the column to use, typically 'Adj Close' if stock ticker
                window                     : time period to use for moving average calculation
                method                     : currently either "Smooth Moving Average (SMA) or
                                             "Exponential Weighted Average (EWA))
                    

            Returns:
                    data (df): A dataframe containing the original data and a new column 'RSI_' + colName
    '''
    delta = df_OHLC[colName].diff(1)
    delta.dropna(inplace=True)

    positive, negative = delta.copy(), delta.copy()

    positive[positive < 0] = 0
    negative[negative > 0] = 0

    if method == 'SMA':            
        average_gain = positive.rolling(window=window).mean()
        average_loss = abs(negative.rolling(window=window).mean())
    elif method == 'EWA':
        average_gain = positive.ewm(span=window-1, adjust=False).mean()
        average_loss = abs(negative.ewm(span=window-1, adjust=False).mean())

    relative_strength = average_gain / average_loss
    relative_strength = relative_strength.apply(lambda x: 1 if math.isinf(x) else x)
    relative_strength = relative_strength.apply(lambda x: 1 if math.isnan(x) else x)

    # RSI = 100.0 - (100.0 / (1.0 + relative_strength))    
    # create a new column for RSI and return the df
    
    newColName = 'RSI_' + method + '_'  + colName
    df_OHLC[newColName] = pd.Series(100 - (100 / (1 + relative_strength)), name=newColName)
    
    return df_OHLC
