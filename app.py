import plotly.graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS
import numpy as np
from graph import make_diffusivities
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("H-transport properties dashboard"),
                        html.H5("Rémi Delaporte-Mathurin"),
                    ],
                    width=True,
                ),
            ],
            align="end",
        ),
        html.Hr(),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Diffusivity",
                    value="tab-1",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Filter by material:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["tungsten", "copper", "cucrzr"],
                                            ["tungsten"],
                                            multi=True,
                                            id="material_filter_diffusivities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by isotope:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["H", "D", "T"],
                                            ["H"],
                                            multi=True,
                                            id="isotope_filter_diffusivities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by author:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["Frauenfelder", "Heinola", "Fernandez"],
                                            ["Frauenfelder"],
                                            multi=True,
                                            id="author_filter_diffusivities",
                                        ),
                                        html.Br(),
                                        html.Label("Filter by year:"),
                                        dcc.RangeSlider(
                                            id="year_filter_diffusivities",
                                            min=1950,
                                            max=2021,
                                            step=1,
                                            value=[1950, 2021],
                                            marks={
                                                int(i): str(i)
                                                for i in np.arange(1950, 2021, step=10)
                                            },
                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": True,
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Compute mean curve",
                                                    id="mean_button",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                                dbc.Button(
                                                    "Extract data",
                                                    id="extract_button",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="graph1",
                                            figure=make_diffusivities(),
                                            style={"width": "150vh", "height": "70vh"},
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Solubility",
                    value="tab-2",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Filter by material:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["tungsten", "copper", "cucrzr"],
                                            ["tungsten"],
                                            multi=True,
                                        ),
                                        html.Br(),
                                        html.Label("Filter by isotope:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["H", "D", "T"],
                                            ["H"],
                                            multi=True,
                                        ),
                                        html.Br(),
                                        html.Label("Filter by author:"),
                                        dcc.RadioItems(
                                            ["All", "Custom"],
                                            "All",
                                            inputStyle={
                                                "margin-left": "20px",
                                                "margin-right": "2px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            ["Frauenfelder", "Heinola", "Fernandez"],
                                            ["Frauenfelder"],
                                            multi=True,
                                        ),
                                        html.Br(),
                                        html.Label("Filter by year:"),
                                        dcc.RangeSlider(
                                            id="year2",
                                            min=1950,
                                            max=2021,
                                            step=1,
                                            value=[1950, 2021],
                                            marks={
                                                int(i): str(i)
                                                for i in np.arange(1950, 2021, step=10)
                                            },
                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": True,
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Compute mean curve",
                                                    id="mean_button2",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                                dbc.Button(
                                                    "Extract data",
                                                    id="extract_button2",
                                                    color="primary",
                                                    style={"margin": "5px"},
                                                    n_clicks_timestamp="0",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="graph2",
                                            figure=make_diffusivities(),
                                            style={"width": "150vh", "height": "70vh"},
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
)
app.layout = layout


# callback filter material diffusivity
@app.callback(
    dash.Output("graph1", "figure"),
    dash.Input("material_filter_diffusivities", "value"),
    dash.Input("isotope_filter_diffusivities", "value"),
    dash.Input("author_filter_diffusivities", "value"),
    dash.Input("year_filter_diffusivities", "value"),
)
def update_graph(
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
):
    return make_diffusivities(
        materials=material_filter_diffusivities,
        authors=author_filter_diffusivities,
        isotopes=isotope_filter_diffusivities,
        years=year_filter_diffusivities,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
