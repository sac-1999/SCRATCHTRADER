# app.py

from dash import Dash, html, Output, Input, State, MATCH, ctx, ALL
from heatmap import get_heatmap_layout, plot_stocks
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
    get_heatmap_layout()
])

# @app.callback(
#     Output("heatmap-plots", "children"),
#     Input("update-interval", "n_intervals")
# )
# def update_plots(n):
#     return plot_layout()

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
