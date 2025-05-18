# app.py

from dash import Dash, html, Output, Input, State, MATCH, ctx, ALL
from heatmap import get_heatmap_layout, plot_layout, plot_stock
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

@app.callback(
    Output("heatmap-plots", "children"),
    Input("update-interval", "n_intervals")
)
def update_plots(n):
    return plot_layout()


@app.callback(
    Output('dummy-output', 'children'),
    Input({'type': 'sector-checklist', 'index': ALL}, 'value')
)
def get_selected_stocks(all_selected_lists):
    return f"Selected stocks: {all_selected_lists}"

@app.callback(
    Output('selected-stocks-store', 'data'),
    Input({'type': 'sector-checklist', 'index': ALL}, 'value'),
)
def update_heatmap(selected_stocks):
    if not selected_stocks:
        return []
    return selected_stocks

# @app.callback(
#     Output('selected-stocks-store', 'data'),
#     Input({'type': 'sector-checklist', 'index': ALL}, 'value'),
#     prevent_initial_call=False  # Allow this callback to run after the initial load
# )
# def update_stored_selections(selected_stocks_list):
#     all_selected_stocks = [stock for sector_stocks in selected_stocks_list for stock in sector_stocks]
#     print(all_selected_stocks)
#     return all_selected_stocks


if __name__ == '__main__':
    app.run(debug=True)
