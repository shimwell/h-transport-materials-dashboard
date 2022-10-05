import numpy as np
from layout import layout
from graph import (
    all_diffusivities,
    all_solubilities,
    make_diffusivities,
    make_solubilities,
    make_graph_diffusivities,
    make_graph_solubilities,
    add_mean_value,
    add_mean_value_solubilities,
    MIN_YEAR_SOL,
    MAX_YEAR_SOL,
    MIN_YEAR_DIFF,
    MAX_YEAR_DIFF,
    make_figure_prop_per_year,
)

from citations import make_citations_graph

import h_transport_materials as htm

from export import create_data_as_dict, generate_python_code

from tab import materials_options

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

app.layout = layout

for group in ["diffusivity", "solubility"]:

    @app.callback(
        dash.Output(f"graph_nb_citations_{group}", "figure"),
        dash.Input(f"graph_{group}", "figure"),
        dash.Input(f"radio_citations_{group}", "value"),
        dash.State(f"material_filter_{group}", "value"),
        dash.State(f"isotope_filter_{group}", "value"),
        dash.State(f"author_filter_{group}", "value"),
        dash.State(f"year_filter_{group}", "value"),
    )
    def make_figure(
        figure,
        radio_citations,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        if group == "diffusivity":
            diffusitivites = make_diffusivities(
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return make_citations_graph(
                diffusitivites, per_year=radio_citations == "Per year"
            )
        elif group == "solubility":
            solubilities = make_solubilities(
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return make_citations_graph(
                solubilities, per_year=radio_citations == "Per year"
            )


for group in ["diffusivity", "solubility"]:

    @app.callback(
        dash.Output(f"material_filter_{group}", "value"),
        dash.Input(f"add_all_materials_{group}", "n_clicks"),
    )
    def add_all_material(n_clicks):
        if n_clicks:
            return materials_options
        else:
            return dash.no_update


@app.callback(
    dash.Output("author_filter_diffusivity", "value"),
    dash.Input("add_all_authors_diffusivity", "n_clicks"),
)
def add_all_authors(n_clicks):
    if n_clicks:
        return np.unique([D.author.capitalize() for D in all_diffusivities]).tolist()
    else:
        return dash.no_update


# callback filter material diffusivity
@app.callback(
    dash.Output("graph_diffusivity", "figure"),
    dash.Output("graph_prop_per_year_diffusivity", "figure"),
    dash.Input("material_filter_diffusivity", "value"),
    dash.Input("isotope_filter_diffusivity", "value"),
    dash.Input("author_filter_diffusivity", "value"),
    dash.Input("year_filter_diffusivity", "value"),
    dash.Input("mean_button_diffusivity", "n_clicks"),
)
def update_graph(
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
    mean_button_diffusivity,
):
    diffusitivites = make_diffusivities(
        materials=material_filter_diffusivities,
        authors=author_filter_diffusivities,
        isotopes=isotope_filter_diffusivities,
        years=year_filter_diffusivities,
    )

    all_time_diffusivities = make_diffusivities(
        materials=material_filter_diffusivities,
        authors=author_filter_diffusivities,
        isotopes=isotope_filter_diffusivities,
        years=[MIN_YEAR_DIFF, MAX_YEAR_DIFF],
    )
    figure = make_graph_diffusivities(diffusitivites)
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "mean_button_diffusivity.n_clicks":
        add_mean_value(diffusitivites, figure)

    return figure, make_figure_prop_per_year(
        all_time_diffusivities, step=5, selected_years=year_filter_diffusivities
    )


@app.callback(
    dash.Output("author_filter_solubility", "value"),
    dash.Input("add_all_authors_solubility", "n_clicks"),
)
def add_all_authors(n_clicks):
    if n_clicks:
        return np.unique([S.author.capitalize() for S in all_solubilities]).tolist()
    else:
        return dash.no_update


# callback filters solubility
@app.callback(
    dash.Output("graph_solubility", "figure"),
    dash.Output("graph_prop_per_year_solubility", "figure"),
    dash.Input("material_filter_solubility", "value"),
    dash.Input("isotope_filter_solubility", "value"),
    dash.Input("author_filter_solubility", "value"),
    dash.Input("year_filter_solubility", "value"),
    dash.Input("mean_button_solubility", "n_clicks"),
)
def update_solubility_graph(
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
    mean_button_solubility,
):
    solubilities = make_solubilities(
        materials=material_filter_solubilities,
        authors=author_filter_solubilities,
        isotopes=isotope_filter_solubilities,
        years=year_filter_solubilities,
    )
    all_time_solubilities = make_solubilities(
        materials=material_filter_solubilities,
        authors=author_filter_solubilities,
        isotopes=isotope_filter_solubilities,
        years=[MIN_YEAR_SOL, MAX_YEAR_SOL],
    )
    figure = make_graph_solubilities(solubilities)
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "mean_button_solubility.n_clicks":
        add_mean_value_solubilities(solubilities, figure)

    return figure, make_figure_prop_per_year(
        all_time_solubilities, step=5, selected_years=year_filter_solubilities
    )


# extract data buttons
@app.callback(
    dash.Output("download-text_diffusivity", "data"),
    dash.Input("extract_button_diffusivity", "n_clicks"),
    dash.Input("material_filter_diffusivity", "value"),
    dash.Input("isotope_filter_diffusivity", "value"),
    dash.Input("author_filter_diffusivity", "value"),
    dash.Input("year_filter_diffusivity", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "extract_button_diffusivity.n_clicks":
        diffusivities = make_diffusivities(
            materials=material_filter_diffusivities,
            authors=author_filter_diffusivities,
            isotopes=isotope_filter_diffusivities,
            years=year_filter_diffusivities,
        )
        return dict(
            content=create_data_as_dict(diffusivities),
            filename="data.json",
        )


@app.callback(
    dash.Output("download-text_solubility", "data"),
    dash.Input("extract_button_solubility", "n_clicks"),
    dash.Input("material_filter_solubility", "value"),
    dash.Input("isotope_filter_solubility", "value"),
    dash.Input("author_filter_solubility", "value"),
    dash.Input("year_filter_solubility", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "extract_button_solubility.n_clicks":
        solubilities = make_solubilities(
            materials=material_filter_solubilities,
            authors=author_filter_solubilities,
            isotopes=isotope_filter_solubilities,
            years=year_filter_solubilities,
        )
        return dict(
            content=create_data_as_dict(solubilities),
            filename="data.json",
        )


# callbacks for python buttons
@app.callback(
    dash.Output("download-python_solubility", "data"),
    dash.Input("python_button_solubility", "n_clicks"),
    dash.Input("material_filter_solubility", "value"),
    dash.Input("isotope_filter_solubility", "value"),
    dash.Input("author_filter_solubility", "value"),
    dash.Input("year_filter_solubility", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_solubilities,
    isotope_filter_solubilities,
    author_filter_solubilities,
    year_filter_solubilities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "python_button_solubility.n_clicks":

        return dict(
            content=generate_python_code(
                materials=material_filter_solubilities,
                isotopes=isotope_filter_solubilities,
                authors=author_filter_solubilities,
                yearmin=year_filter_solubilities[0],
                yearmax=year_filter_solubilities[1],
                group="solubilities",
            ),
            filename="script.py",
        )


@app.callback(
    dash.Output("download-python_diffusivity", "data"),
    dash.Input("python_button_diffusivity", "n_clicks"),
    dash.Input("material_filter_diffusivity", "value"),
    dash.Input("isotope_filter_diffusivity", "value"),
    dash.Input("author_filter_diffusivity", "value"),
    dash.Input("year_filter_diffusivity", "value"),
    prevent_initial_call=True,
)
def func(
    n_clicks,
    material_filter_diffusivities,
    isotope_filter_diffusivities,
    author_filter_diffusivities,
    year_filter_diffusivities,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "python_button_diffusivity.n_clicks":

        return dict(
            content=generate_python_code(
                materials=material_filter_diffusivities,
                isotopes=isotope_filter_diffusivities,
                authors=author_filter_diffusivities,
                yearmin=year_filter_diffusivities[0],
                yearmax=year_filter_diffusivities[1],
                group="diffusivities",
            ),
            filename="script.py",
        )


@app.callback(
    dash.Output("modal", "is_open"),
    dash.Input("open-sm", "n_clicks"),
    dash.State("modal", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    dash.Output("modal_add_diffusivity", "is_open"),
    dash.Input("add_property_diffusivity", "n_clicks"),
    dash.Input("submit_new_diffusivity", "n_clicks"),
    dash.State("modal_add_diffusivity", "is_open"),
    dash.State("new_diffusivity_pre_exp", "value"),
    dash.State("new_diffusivity_act_energy", "value"),
    dash.State("new_diffusivity_author", "value"),
    dash.State("new_diffusivity_year", "value"),
    dash.State("new_diffusivity_isotope", "value"),
    dash.State("new_diffusivity_material", "value"),
    prevent_initial_call=True,
)
def toggle_modal(
    n1,
    n2,
    is_open,
    new_diffusivity_pre_exp,
    new_diffusivity_act_energy,
    new_diffusivity_author,
    new_diffusivity_year,
    new_diffusivity_isotope,
    new_diffusivity_material,
):
    if is_open and None in [
        new_diffusivity_pre_exp,
        new_diffusivity_act_energy,
        new_diffusivity_author,
        new_diffusivity_year,
        new_diffusivity_isotope,
        new_diffusivity_material,
    ]:
        return is_open
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    dash.Output("modal_add_solubility", "is_open"),
    dash.Input("add_property_solubility", "n_clicks"),
    dash.Input("submit_new_solubility", "n_clicks"),
    dash.State("new_solubility_pre_exp", "value"),
    dash.State("new_solubility_act_energy", "value"),
    dash.State("new_solubility_author", "value"),
    dash.State("new_solubility_year", "value"),
    dash.State("new_solubility_isotope", "value"),
    dash.State("new_solubility_material", "value"),
    dash.State("modal_add_solubility", "is_open"),
    prevent_initial_call=True,
)
def toggle_modal(
    n1,
    n2,
    is_open,
    new_solubility_pre_exp,
    new_solubility_act_energy,
    new_solubility_author,
    new_solubility_year,
    new_solubility_isotope,
    new_solubility_material,
):
    if is_open and None in [
        new_solubility_pre_exp,
        new_solubility_act_energy,
        new_solubility_author,
        new_solubility_year,
        new_solubility_isotope,
        new_solubility_material,
    ]:
        return is_open
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    dash.Output("material_filter_diffusivity", "options"),
    dash.Output("author_filter_diffusivity", "options"),
    dash.Output("error_message_new_diffusivity", "children"),
    dash.Input("submit_new_diffusivity", "n_clicks"),
    dash.Input("material_filter_diffusivity", "value"),
    dash.State("new_diffusivity_pre_exp", "value"),
    dash.State("new_diffusivity_act_energy", "value"),
    dash.State("new_diffusivity_author", "value"),
    dash.State("new_diffusivity_year", "value"),
    dash.State("new_diffusivity_isotope", "value"),
    dash.State("new_diffusivity_material", "value"),
    dash.State("new_diffusivity_range_low", "value"),
    dash.State("new_diffusivity_range_high", "value"),
    prevent_initial_call=True,
)
def add_diffusivity(
    n_clicks,
    material_filter_diffusivities,
    new_diffusivity_pre_exp,
    new_diffusivity_act_energy,
    new_diffusivity_author,
    new_diffusivity_year,
    new_diffusivity_isotope,
    new_diffusivity_material,
    new_diffusivity_range_low,
    new_diffusivity_range_high,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "submit_new_diffusivity.n_clicks":
        if None in [
            new_diffusivity_pre_exp,
            new_diffusivity_act_energy,
            new_diffusivity_author,
            new_diffusivity_year,
            new_diffusivity_isotope,
            new_diffusivity_material,
        ]:
            return dash.no_update, dash.no_update, "Error!"
        if (new_diffusivity_range_low, new_diffusivity_range_high) == (None, None):
            (new_diffusivity_range_low, new_diffusivity_range_high) = (300, 1200)
        new_property = htm.ArrheniusProperty(
            pre_exp=new_diffusivity_pre_exp,
            act_energy=new_diffusivity_act_energy,
            author=new_diffusivity_author.lower(),
            year=new_diffusivity_year,
            isotope=new_diffusivity_isotope,
            material=new_diffusivity_material,
            range=(new_diffusivity_range_low, new_diffusivity_range_high),
        )
        all_diffusivities.properties.append(new_property)

    all_authors = np.unique(
        [
            D.author.capitalize()
            for D in all_diffusivities
            if D.material in material_filter_diffusivities
        ]
    ).tolist()
    all_materials = np.unique([D.material.lower() for D in all_diffusivities]).tolist()

    return all_materials, all_authors, ""


@app.callback(
    dash.Output("material_filter_solubility", "options"),
    dash.Output("author_filter_solubility", "options"),
    dash.Output("error_message_new_solubility", "children"),
    dash.Input("submit_new_solubility", "n_clicks"),
    dash.Input("material_filter_solubility", "value"),
    dash.State("new_solubility_pre_exp", "value"),
    dash.State("new_solubility_act_energy", "value"),
    dash.State("new_solubility_author", "value"),
    dash.State("new_solubility_year", "value"),
    dash.State("new_solubility_isotope", "value"),
    dash.State("new_solubility_material", "value"),
    dash.State("new_solubility_range_low", "value"),
    dash.State("new_solubility_range_high", "value"),
    prevent_initial_call=True,
)
def add_solubility(
    n_clicks,
    material_filter_solubilities,
    new_solubility_pre_exp,
    new_solubility_act_energy,
    new_solubility_author,
    new_solubility_year,
    new_solubility_isotope,
    new_solubility_material,
    new_solubility_range_low,
    new_solubility_range_high,
):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if changed_id == "submit_new_diffusivity.n_clicks":
        if None in [
            new_solubility_pre_exp,
            new_solubility_act_energy,
            new_solubility_author,
            new_solubility_year,
            new_solubility_isotope,
            new_solubility_material,
        ]:
            return dash.no_update, dash.no_update, "Error!"
        if (new_solubility_range_low, new_solubility_range_high) == (None, None):
            (new_solubility_range_low, new_solubility_range_high) = (300, 1200)
        new_property = htm.ArrheniusProperty(
            pre_exp=new_solubility_pre_exp,
            act_energy=new_solubility_act_energy,
            author=new_solubility_author.lower(),
            year=new_solubility_year,
            isotope=new_solubility_isotope,
            material=new_solubility_material,
            range=(new_solubility_range_low, new_solubility_range_high),
        )
        all_solubilities.properties.append(new_property)
    all_authors = np.unique(
        [
            D.author.capitalize()
            for D in all_solubilities
            if D.material in material_filter_solubilities
        ]
    ).tolist()
    all_materials = np.unique([D.material.lower() for D in all_solubilities]).tolist()

    return all_materials, all_authors, ""


if __name__ == "__main__":
    app.run_server(debug=True)
