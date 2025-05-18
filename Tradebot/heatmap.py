# heatmap.py

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from data import sector_stocks, stockdetails  

def fetch_sector_details(stocks):
    stock_changes = []
    failed_stocks = []
    for stock in stocks:
        try:
            low = stockdetails[stock]['low']
            high = stockdetails[stock]['high']
            close = stockdetails[stock]['close']
            stock_changes.append((stock, low, 0, high, close))
        except Exception as e:
            failed_stocks.append((stock, 0, 0, 0, 0))
    stock_changes.sort(key=lambda x: x[4], reverse=True)
    stock_changes.extend(failed_stocks)
    return np.array(stock_changes)


def plot_stocks(stocks, sector="Stock Performance"):
    stock_changes = fetch_sector_details(stocks)
    fig = go.Figure(data=[go.Candlestick(
        x=stock_changes[:, 0],
        open=stock_changes[:, 2],
        high=stock_changes[:, 3],
        low=stock_changes[:, 1],
        close=stock_changes[:, 4],
        increasing_line_color="green",
        decreasing_line_color="red"
    )])
    
    fig.update_layout(
        xaxis=dict(
            tickangle=90,  # Rotates labels by -45 degrees
            tickmode='auto',  # Automatically adjusts tick labels
            automargin=False  # Ensures labels are not cut off
        ),
        yaxis=dict(ticksuffix='%'),
        margin=dict(t=30, b=30, l=30, r=30),
        height=250,
            xaxis_rangeslider_visible=False,
        )
    
    wrapped_labels = [label.replace(' ', '<br>') for label in stock_changes[:, 0]]
    fig.update_xaxes(
        tickmode='array',
        tickvals=stock_changes[:, 0],
        ticktext=wrapped_labels,
        tickfont=dict(
            size=10,  
            family='Arial, sans-serif',
            color='black'
        )
    )

    return html.Div([html.Span(sector, className="heatmap-sector-title"),
        dcc.Graph(figure=fig, config={'displayModeBar': False})], className="heatmap_item")


def sector_layout(sector):
    return html.Div([
        html.Span(sector, className='sector-title'),
        html.Div([
            dcc.Checklist(
                id={'type': 'sector-checklist', 'index': sector},  # ✅ unique ID
                options=[{'label': stock, 'value': stock} for stock in sector_stocks[sector]],
                value=[stock for stock in sector_stocks[sector]],  # or pre-tick some
                className='sector-checklist'
            )
        ])
    ], className="sector")


def filter_layout():
    return html.Div([
        sector_layout(sector) for sector in list(sector_stocks.keys())], className="heatmap-filters")

 
def get_heatmap_layout():
    return html.Div([
        dcc.Store(id='selected-stocks-store', storage_type='memory'),
        html.Div(id="heatmap-plots", className='heatmap_plots'),
        filter_layout(),
        dcc.Interval(id='update-interval', interval=1000, n_intervals=0)
    ], className='heatmap_layout')
