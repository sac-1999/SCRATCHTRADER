import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__)
server = app.server

# Define the checklist options for each section
checklist_sections = [
    {
        "title": "Basic Checklist",
        "options": [
            {"label": "Understand what `.DS_Store` files are", "value": "awareness"},
            {"label": "Add `.DS_Store` to .gitignore", "value": "gitignore"},
            {"label": "Remove existing `.DS_Store` files", "value": "remove"},
        ],
        "store_id": "store-dsstore",  # Store ID for this section
        "output_id": "output-dsstore",  # Output ID for this section
    },
    {
        "title": "Advanced Checklist",
        "options": [
            {"label": "Add global Git ignore rule", "value": "global_gitignore"},
            {"label": "Prevent creation on network drives", "value": "network_prevent"},
            {"label": "Set up auto-clean script or Git hook", "value": "automation"},
        ],
        "store_id": "store-advanced",  # Store ID for this section
        "output_id": "output-advanced",  # Output ID for this section
    },
]

app.layout = html.Div([
    html.H1("`.DS_Store` Management Checklists"),

    # Dynamically create each checklist section
    *[html.Div([
        html.H2(section["title"]),
        dcc.Store(id=section["store_id"], storage_type='local'),
        dcc.Checklist(
            id=f'{section["store_id"]}-checklist',
            options=section["options"],
            labelStyle={'display': 'block'}
        ),
        html.Div(id=section["output_id"]),
    ]) for section in checklist_sections]  # Using * to unpack the list of Div elements
])


# ----------- LOAD CALLBACKS (on page load) -----------

@app.callback(
    [Output(f'{section["store_id"]}-checklist', 'value') for section in checklist_sections],
    [Input(section["store_id"], 'data') for section in checklist_sections],
    prevent_initial_call=False  # Allow the callback to run when the page is loaded
)
def load_checklists(*data):
    # Return the data for each checklist or an empty list if not available
    return [data[i] if data[i] else [] for i in range(len(data))]


# ----------- SAVE CALLBACKS (on user change) -----------

@app.callback(
    [Output(section["store_id"], 'data') for section in checklist_sections],
    [Output(section["output_id"], 'children') for section in checklist_sections],
    [Input(f'{section["store_id"]}-checklist', 'value') for section in checklist_sections],
    prevent_initial_call=True  # Prevent execution when loading the page for the first time
)
def save_checklists(*selected_items):
    # Create output for each section dynamically
    data = []
    output = []
    for i, selected in enumerate(selected_items):
        data.append(selected)
        output.append(html.Ul([
            html.Li(f"✅ {item.replace('_', ' ').capitalize()}") for item in selected
        ]) if selected else "Select tasks you've completed.")
    return data, output


if __name__ == '__main__':
    app.run(debug=True)
