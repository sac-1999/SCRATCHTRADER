from dash import Dash, html, dcc, Input, Output, State, ctx

app = Dash()

app.layout = html.Div([
    dcc.Input(id='my-input', type='text', value=''),
    dcc.Store(id='my-store', storage_type='local'),
    html.Div(id='input-loader'), 
    html.Div(id='my-output')
])

@app.callback(
    Output('my-store', 'data'),
    Input('my-input', 'value'),
    prevent_initial_call=True
)
def save_input(value):
    print("Saved to store:", value)
    return value


# ✅ Load value from store into input using one-time trigger
@app.callback(
    Output('my-input', 'value'),
    Input('input-loader', 'children'),
    State('my-store', 'data')
)
def load_input_on_start(_, stored_data):
    print("Loaded from store:", stored_data)
    return stored_data


# ✅ Display current value from store
@app.callback(
    Output('my-output', 'children'),
    Input('my-store', 'data')
)
def show_output(value):
    return f"Stored value: {value}"

if __name__ == '__main__':
    app.run(debug=True)
