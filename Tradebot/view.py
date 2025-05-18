# app.py

from dash import Dash, html, Output, Input, State, MATCH, ctx, ALL
import dash
from heatmap import get_heatmap_layout, plot_stocks
from backtest import *
from intraday import *
import random
from data import sector_stocks

app = Dash(__name__, external_stylesheets=[])

toggle_layout = html.Div([
    html.Button('Heatmap', id="heatmap", className="toggle_button"),
    html.Button('Intraday', id="intraday", className="toggle_button"),
    html.Button('Backtest', id="backtest", className="toggle_button")
], className="toggle")

app.layout = html.Div([
    toggle_layout,
    html.Div(id='layout-container')
])

@app.callback(
    Output('layout-container', 'children'),
    Input('heatmap', 'n_clicks'),
    Input('intraday', 'n_clicks'),
    Input('backtest', 'n_clicks')
)
def display_layout(heatmap_clicks, intraday_clicks, backtest_clicks):
    ctx = dash.callback_context
    val = ctx.triggered[0].get('value')
    if val is None:
        return get_heatmap_layout()
    else:
        print("fwekfgu")
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'heatmap':
            return get_heatmap_layout()
        elif button_id == 'intraday':
            return get_intraday_layout()
        elif button_id == 'backtest':
            return get_backtest_layout()

@app.callback(
    Output("selected-stocks-store", "data"),
    Input({'type': 'sector-checklist', 'index': ALL}, "value"),
    State({'type': 'sector-checklist', 'index': ALL}, "id")  # Retrieve sector names
)
def store_selected_stocks(all_selected_lists, sector_ids):
    sector_selected = {
        sector_id["index"]: stocks for sector_id, stocks in zip(sector_ids, all_selected_lists)
    }    
    return {"selecteditems": sector_selected} 

@app.callback(
    Output("heatmap-plots", "children"),
    Input('update-interval', 'n_intervals'),
    State("selected-stocks-store", "data") 
)
def print_stored_data(n, stored_data):
    allplots = []
    stored_data = stored_data['selecteditems']
    for sector, stocks in stored_data.items():
        # print("1 : ", sector, " -> ",  stocks)
        if len(stocks)>0:
            sectorcharts = plot_stocks(stocks, sector)
            if sectorcharts is not None:
                allplots.append(sectorcharts)
    if not allplots:
        return [html.Div("No stocks selected, please choose some!", className="empty-message")]
    return allplots

if __name__ == '__main__':
    app.run(debug=True)
