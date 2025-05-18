from dash import html
from dash import dcc, html
from datetime import datetime,date, timedelta
from data import *
import pandas as pd
import plotly.graph_objects as go

def get_stock_data():
    df = pd.read_csv('./data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def stock_candle_chart():
    df = get_stock_data()
    weekends = ["sat", "sun"] 
    fig = go.Figure(data=[go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    increasing_line_color='green',
    decreasing_line_color='red')])

    fig.update_layout(
        title='Sample Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            rangebreaks=[
                dict(bounds=weekends)   # Hide weekends
            ]
        ))
    return fig  
  
def backtest_plots():
    return [dcc.Graph(id='candlestick-chart',figure=stock_candle_chart())]


def backtest_filter():
    print(list(stockdetails.keys()))
    return [html.Div(dcc.DatePickerSingle(
        id='entry-date-picker',
        date=datetime.today()-timedelta(30),
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=(datetime.today() - timedelta(1)).date() ,
        initial_visible_month=datetime.today().date(),
        display_format='DD/MM/YYYY'), className='entry-time'),
        
        html.Div(dcc.DatePickerSingle(
        id='exit-date-picker',
        date=datetime.today(),
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=(datetime.today() - timedelta(1)).date() ,
        initial_visible_month=datetime.today().date(),
        display_format='DD/MM/YYYY'), className='exit-time'),
        
        html.Div([
            dcc.Dropdown(
            id='dropdown',
            options=[{'label': item, 'value': item} for item in list(stockdetails.keys())],
            placeholder='item',
            searchable=True)], className="symbol"),
            
        html.Div([html.Button('►', id='play-pause-btn', n_clicks=0), html.Div(id='output')], className='play-pause-button')
        ]

def get_backtest_layout():
    return html.Div([
        html.Div(id = 'backtest-filter', children=backtest_filter(),className = 'backtest-filter'),
        html.Div(id = 'backtest-plots',children=backtest_plots(), className = 'backtest-plots')
    ], className='backtest')