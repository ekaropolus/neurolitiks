import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# Define the layout of the Dash app
layout_scatter = html.Div([
    html.H1('My Dash App'),
    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                go.Scatter(
                    x=[1, 2, 3, 4, 5],
                    y=[2, 4, 1, 3, 5],
                    mode='markers'
                )
            ],
            'layout': go.Layout(
                title='My Scatter Plot',
                xaxis={'title': 'X-axis'},
                yaxis={'title': 'Y-axis'}
            )
        }
    )
])

import dash_cytoscape as cyto

layout = html.Div([
    html.H1('My Network Graph'),
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Graph 1', 'value': 'graph1'},
            {'label': 'Graph 2', 'value': 'graph2'},
            {'label': 'Graph 3', 'value': 'graph3'}
        ],
        value='graph1'
    ),
    cyto.Cytoscape(
        id='graph',
        elements=[
            {'data': {'id': 'n1', 'label': 'Node 1'}},
            {'data': {'id': 'n2', 'label': 'Node 2'}},
            {'data': {'id': 'n3', 'label': 'Node 3'}},
            {'data': {'id': 'e1', 'source': 'n1', 'target': 'n2'}},
            {'data': {'id': 'e2', 'source': 'n2', 'target': 'n3'}},
            {'data': {'id': 'e3', 'source': 'n3', 'target': 'n1'}}
        ],
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '500px'}
    )
])