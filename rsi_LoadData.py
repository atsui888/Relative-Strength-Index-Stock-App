# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 14:12:01 2021

@author: richard chai
https://www.linkedin.com/in/richardchai/
"""
#import pandas as pd
import yfinance as yf

def loadStkData(src,tickers,startDate,endDate,interval='1d', apiKey=None):
    if not src:
        return 'API Provider Required'
    
    if src == 'yFinance':
        return loadData_yFinance(tickers, startDate, endDate, interval)    
        
    
def loadData_yFinance(tickers, startDate, endDate, interval='1d'):    
    '''
    Returns the downloaded stock data.

            Parameters:
                    tickers      (list) : A list of stock ticker symbols    
                    startDate    (str)  : A start date as a string ("yyyy-mm-dd")
                    endDate      (str)  : An end date as a string ("yyyy-mm-dd")
                    interval     (str)  : An string indicating stock data frequency e.g. '1d' for daily

            Returns:
                    data (df): A dataframe containing stock data with multi-index columns
    '''
    # data = yf.download(stockTickers, start="2010-01-01", end="2017-12-31")
    data = yf.download(tickers, start=startDate, end=endDate, interval=interval, \
                       group_by = 'ticker')

    return data