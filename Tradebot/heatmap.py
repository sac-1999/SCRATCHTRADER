# heatmap.py

from dash import html, dcc
import plotly.graph_objects as go
import random
from data import sector_stocks  # assumes sector_stocks is a dict

# 🔹 Dummy plot for a stock with random change
def plot_stock(stock, change):
    fig = go.Figure(go.Bar(
        x=[stock],
        y=[change],
        marker_color='green' if change >= 0 else 'red'
    ))
    fig.update_layout(
        height=250,
        margin=dict(t=30, b=30, l=30, r=30),
        yaxis=dict(ticksuffix='%')
    )
    return html.Div([dcc.Graph(figure=fig, config={'displayModeBar': False})], className="heatmap_item")

# 🔹 Generate layout with random stock plots
def plot_layout():
    return [plot_stock('TCS', round(random.uniform(-2, 2), 2)) for _ in range(10)]

def sector_layout(sector):
    return html.Div([
        html.Span(sector, className='sector-title'),
        html.Div([
            dcc.Checklist(
                id={'type': 'sector-checklist', 'index': sector},  # ✅ unique ID
                options=[{'label': stock, 'value': stock} for stock in sector_stocks[sector]],
                value=[],  # or pre-tick some
                className='sector-checklist'
            )
        ])
    ], className="sector")


def filter_layout():
    return html.Div([
        sector_layout(sector) for sector in list(sector_stocks.keys())], className="heatmap-filters")

 
def get_heatmap_layout():
    return html.Div([
        dcc.Store(id='selected-stocks-store', storage_type='local'),
        html.Div(id='dummy-output', style={'display': 'none'}),
        html.Div(id="heatmap-plots", className='heatmap_plots'),
        filter_layout(),
        dcc.Interval(id='update-interval', interval=100, n_intervals=0)
    ], className='heatmap_layout')
