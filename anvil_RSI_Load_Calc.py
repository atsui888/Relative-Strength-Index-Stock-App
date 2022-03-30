import anvil.server
import yfinance as yf
import pandas as pd
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import tools


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable  
def plotly_hello_world():
  import plotly.express as px
  df = px.data.gapminder().query("country=='Canada'")
  fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
  fig.show()
  return fig
  

def dict2series(dd, colName_OHLC='adj_close'):
    s = pd.Series(dd, name=colName_OHLC)
    s.index.name='Date'
    s.sort_index(inplace=True)
    return s

def dict2df(dd, colName_OHLC='adj_close'):
    df = pd.DataFrame(dd.items(), columns=['date', colName_OHLC])
    #df['date'] = df['date'].astype('datetime64[ns]')    
    # raw_data['Mycol'] =  pd.to_datetime(raw_data['Mycol'], infer_datetime_format=True)
    df.date=pd.to_datetime(df.date, format='%Y-%m-%d')
    #df.date=pd.to_datetime(df.date, infer_datetime_format=True)
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df   

       
@anvil.server.callable   
def loadData_yFinance(ticker, OHLC, startDate, endDate, rsi_mthd, window, interval='1d'):    
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
    data = yf.download(ticker, start=startDate, end=endDate, interval=interval, \
                       group_by = 'ticker')
    
    data.index = data.index.strftime('%Y-%m-%d')  # change index from datetime object to string
    data_X = data.index.values.tolist()
    data_Y = list(data[OHLC].values)

    
    data = data[OHLC].to_dict()
    rsi_X, rsi_Y = RSI_Calc(data, rsi_mthd, window)
    #fig = plotly_Plot_RSA(ticker, data, data_rsi, OHLC,rsi_mthd=rsi_mthd, overSoldTres=20, overBoughtTres=80)
    
    return data_X, data_Y, rsi_X, rsi_Y
    # the next 3 lines are used if I wish to return a dict
    #data.index = data.index.strftime('%Y-%m-%d')  # change index from datetime object to string
#     # return a dictionary (key: date string, value: numeric stock price)
#     return data[OHLC].to_dict()


def RSI_Calc(dict_OHLC, method="SMA", window = 14):
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
    
    df_OHLC = pd.Series(dict_OHLC, name='price')
    df_OHLC.index.name='Date'
    #df_OHLC.index = df_OHLC.index.astype('datetime64[ns]')  
    df_OHLC.sort_index(inplace=True)
    
    delta = df_OHLC.diff(1)
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
    
    df_OHLC = pd.Series(100 - (100 / (1 + relative_strength)), name='price')
    
    X = df_OHLC.index.values.tolist()
    y = list(df_OHLC.values)
    
    return X,y
    # return df_OHLC  # anvil front end cannot accept pandas dataframe, hence need to return a dict.
    #return df_OHLC.to_dict()
  

def plotly_Plot_RSA(ticker,data,data_rsi,ohlc_col_name,height=680,width=800, rsi_mthd='SMA', overSoldTres=20, overBoughtTres=80):       
    dfStk = dict2df(data, colName_OHLC=ohlc_col_name)
    dfStk_RSI = dict2df(data_rsi, colName_OHLC=ohlc_col_name)
    
    #return dfStk.index.to_list()
    
    fig = make_subplots(rows=2, cols=1,vertical_spacing=0.13,
                   subplot_titles=(ohlc_col_name, "RSI Values"),
                   column_widths=[1.0], row_heights=[0.5,0.5])

    fig.append_trace(go.Scatter(
        x=dfStk.index,
        y=dfStk[ohlc_col_name],
        mode='lines',
        #name='Adj Close ($)'  # default name is 'trace 0'
        name = ohlc_col_name
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=dfStk_RSI.index,
        y=dfStk_RSI[ohlc_col_name],
        line_color="forestgreen",
        line_width=1,
        mode='lines+markers',
        #mode='lines',
        name='RSI Value'
    ), row=2, col=1)


    if rsi_mthd == 'SMA' or rsi_mthd == 'EWA':
        fig.add_hline(y=20, annotation_text="RSI = 20", annotation_position="bottom right",
              line_width=2, line_dash="dash", line_color="red", row=2,col=1)
        fig.add_hline(y=80, annotation_text="RSI = 80", annotation_position="bottom right",
               line_width=2, line_dash="dash", line_color="red", row=2,col=1)

        for i, row in dfStk_RSI.iterrows():
            if row[ohlc_col_name] < overSoldTres:
                fig.add_annotation(x=i, y=row[ohlc_col_name],text="OverSold",
                                   font=dict(color="#ff0000"), opacity=0.8, ax=-34,ay=24,
                                   showarrow=True,arrowhead=1, arrowcolor="#FF0000", row=2,col=1) 
            if row[ohlc_col_name] > overBoughtTres:
                fig.add_annotation(x=i, y=row[ohlc_col_name],text="OverBought",
                                   font=dict(color="#ff0000"), opacity=0.8, ax=-34,ay=-24,
                                   showarrow=True,arrowhead=1,arrowcolor="#FF0000", row=2,col=1) 
        
    fig.update_layout(
        title_text= f'Stock Ticker: {ticker} from {dfStk.index[0].date()} to {dfStk.index[-1].date()}',        
        template='simple_white', height=height) 
        # height=height, width=width, autosize=True
    
    #fig.show()
    return fig   


    