"""
@author: richard chai
https://www.linkedin.com/in/richardchai/
"""


from ._anvil_designer import RSI_AppTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import datetime as dt


class RSI_App(RSI_AppTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    #self.tickers = sorted(["FB", "AAPL", "AMZN", "GOOGL", "MSFT","TSLA"])
    self.ticker = ""
    self.OHLC = ""
    #startDate = dt.date(2015,1,1)    
    self.startDate = dt.datetime.now() - dt.timedelta(days=1*365)    
    self.endDate = dt.datetime.now()
    self.RSI_Mthd = ""
    self.window = 14
    self.src = 'yFinance'
    self.interval='1d'
             

  def btn_get_stock_data_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    self.fig = anvil.server.call('plotly_hello_world')
    
    
    self.ticker = self.dd_ticker.selected_value
    self.OHLC = self.dd_OHLC.selected_value
    if self.dtd_Start.date is None:
      self.startDate = dt.datetime.now() - dt.timedelta(days=3*365)
    else: self.startDate = self.dtd_Start.date
    # endDate = dt.date(2015,12,31)
    if self.dtd_End.date is None:
      self.endDate = dt.datetime.now()
    else: self.endDate = self.dtd_End.date
    self.RSI_Mthd = self.dd_RSI_Mthd.selected_value
    self.window = int(self.dd_Window.selected_value)
   
    data_X, data_Y, rsi_X, rsi_Y = anvil.server.call('loadData_yFinance',self.ticker,self.OHLC
                                  ,self.startDate, self.endDate,                                   
                                  self.RSI_Mthd, self.window, self.interval)        
    data_Y = [round(i,2) for i in data_Y]
    rsi_Y  = [round(i,2) for i in rsi_Y]
    
    # plot ticker price
    self.plot_ticker.layout = {
      'title': 'Stock Price',
      'xaxis': { 'title': 'date' }
    }
    self.plot_ticker.layout.yaxis.title = 'price'
#     self.plot_ticker.layout.annotations = [
#       dict(
#         text = 'Simple annotation',
#         x = 0,
#         xref = 'paper',
#         y = 0,
#         yref = 'paper'
#       )
#     ]
    # Plot some data
    self.plot_ticker.data = [
      go.Scatter(
        x = data_X,  # rsi_X,
        y = data_Y, # rsi_Y,
        marker = dict(
          color= 'rgb(16, 32, 77)'
        )
      )      
#       ,go.Bar(
#         x = [1, 2, 3],
#         y = [3, 1, 6],
#         name = 'Bar Chart Example'
#       )
    ]

    # plot RSI
#     self.plot_rsi.layout = {
#       'title': 'RSI',
#       'xaxis': { 'title': 'date' }
#     }
    self.plot_rsi.layout = {
      'title': 'RSI',
      'xaxis': { 'title': 'date' }
    }

    self.plot_rsi.layout.yaxis.title = 'rsi'
    self.plot_rsi.layout.annotations = [
      dict(
        text = 'Overbought',
        x = 0, 
        xref = 'paper',
        y = 0.8,
        yref = 'paper'
      ),
      dict(
        text = 'Oversold',
        x = 0, 
        xref = 'paper',
        y = 0.2,
        yref = 'paper'
      )
    ]
    
    # Plot some data
    self.plot_rsi.data = [
      go.Scatter(
        x = rsi_X,
        y = rsi_Y,
        marker = dict(
          color= 'rgb(16, 32, 77)',
          colorscale='Viridis',
          showscale=True
        )
      )
#       ,go.Bar(
#         x = [1, 2, 3],
#         y = [3, 1, 6],
#         name = 'Bar Chart Example'
#       )
    ]
    


    pass

  def plot_rsi_hover(self, points, **event_args):
    """This method is called when a data point is hovered."""
    self.lbl_temp.text=f"User hovered over x:{points[0]['x']} and y:{points[0]['y']}"
    pass



