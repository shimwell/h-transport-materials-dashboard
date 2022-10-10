import numpy as np
import dash

from .export import create_data_as_dict, generate_python_code

from .tab import materials_options, TABLE_KEYS

from .graph import (
    all_diffusivities,
    all_solubilities,
    make_diffusivities,
    make_piechart_author,
    make_piechart_isotopes,
    make_solubilities,
    make_graph_diffusivities,
    make_piechart_materials,
    make_graph_solubilities,
    add_mean_value_diffusivities,
    add_mean_value_solubilities,
    MIN_YEAR_SOL,
    MAX_YEAR_SOL,
    MIN_YEAR_DIFF,
    MAX_YEAR_DIFF,
    make_figure_prop_per_year,
    make_citations_graph,
)

import h_transport_materials as htm


group_to_all_props = {"diffusivity": all_diffusivities, "solubility": all_solubilities}
group_to_make = {"diffusivity": make_diffusivities, "solubility": make_solubilities}


def create_make_citations_figure_function(group):
    def make_citations_figure(
        figure,
        per_year,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        return make_citations_graph(properties_group, per_year=per_year)

    return make_citations_figure


def create_add_all_materials_function(group):
    def add_all_materials(n_clicks):
        if n_clicks:
            return materials_options
        else:
            return dash.no_update

    return add_all_materials


def create_add_all_authors_function(group):
    def add_all_authors(n_clicks):

        if n_clicks:
            return np.unique(
                [prop.author.capitalize() for prop in group_to_all_props[group]]
            ).tolist()
        else:
            return dash.no_update

    return add_all_authors


def create_update_entries_per_year_graph_function(group):
    def update_entries_per_year_graph(
        figure, material_filter, isotope_filter, author_filter, year_filter
    ):
        if group == "diffusivity":
            min_year, max_year = MIN_YEAR_DIFF, MAX_YEAR_DIFF
        elif group == "solubility":
            min_year, max_year = MIN_YEAR_SOL, MAX_YEAR_SOL
        all_time_properties = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=[min_year, max_year],
        )
        return make_figure_prop_per_year(
            all_time_properties, step=5, selected_years=year_filter
        )

    return update_entries_per_year_graph


def create_update_graph_function(group):
    def update_graph(
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
        mean_button,
        colour_by,
    ):
        if group == "diffusivity":
            make_graph = make_graph_diffusivities
            add_mean = add_mean_value_diffusivities
        elif group == "solubility":
            make_graph = make_graph_solubilities
            add_mean = add_mean_value_solubilities

        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        figure = make_graph(properties_group, colour_by)
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"mean_button_{group}.n_clicks":
            add_mean(properties_group, figure)

        return figure

    return update_graph


def create_make_download_data_function(group):
    def make_download_data(
        n_clicks,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):

        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"extract_button_{group}.n_clicks":
            properties_group = group_to_make[group](
                materials=material_filter,
                authors=author_filter,
                isotopes=isotope_filter,
                years=year_filter,
            )
            return dict(
                content=create_data_as_dict(properties_group),
                filename="data.json",
            )

    return make_download_data


def make_download_python_callback(group):
    def download_python(
        n_clicks,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"python_button_{group}.n_clicks":

            return dict(
                content=generate_python_code(
                    materials=material_filter,
                    isotopes=isotope_filter,
                    authors=author_filter,
                    yearmin=year_filter[0],
                    yearmax=year_filter[1],
                    group=group,
                ),
                filename="script.py",
            )

    return download_python


def make_toggle_modal_function(group):
    def toggle_modal(
        n1,
        n2,
        is_open,
        new_prop_pre_exp,
        new_prop_act_energy,
        new_prop_author,
        new_prop_year,
        new_prop_isotope,
        new_prop_material,
    ):
        if is_open and None in [
            new_prop_pre_exp,
            new_prop_act_energy,
            new_prop_author,
            new_prop_year,
            new_prop_isotope,
            new_prop_material,
        ]:
            return is_open
        if n1 or n2:
            return not is_open
        return is_open

    return toggle_modal


def make_add_property(group):
    def add_property(
        n_clicks,
        material_filter,
        new_pre_exp,
        new_act_energy,
        new_author,
        new_year,
        new_isotope,
        new_material,
        new_range_low,
        new_range_high,
    ):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if changed_id == f"submit_new_{group}.n_clicks":
            if None in [
                new_pre_exp,
                new_act_energy,
                new_author,
                new_year,
                new_isotope,
                new_material,
            ]:
                return dash.no_update, dash.no_update, "Error!"
            if (new_range_low, new_range_high) == (None, None):
                (new_range_low, new_range_high) = (300, 1200)
            new_property = htm.ArrheniusProperty(
                pre_exp=new_pre_exp,
                act_energy=new_act_energy,
                author=new_author.lower(),
                year=new_year,
                isotope=new_isotope,
                material=new_material,
                range=(new_range_low, new_range_high),
            )
            group_to_all_props[group].properties.append(new_property)

        all_authors = np.unique(
            [
                prop.author.capitalize()
                for prop in group_to_all_props[group]
                if prop.material in material_filter
            ]
        ).tolist()
        all_materials = np.unique(
            [prop.material.lower() for prop in group_to_all_props[group]]
        ).tolist()

        return all_materials, all_authors, ""

    return add_property


def create_update_piechart_material_function(group):
    def update_piechart_material(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_materials(properties_group)

    return update_piechart_material


def create_update_piechart_isotopes_function(group):
    def update_piechart_isotope(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_isotopes(properties_group)

    return update_piechart_isotope


def create_update_piechart_authors_function(group):
    def update_piechart_author(
        figure,
        material_filter,
        isotope_filter,
        author_filter,
        year_filter,
    ):
        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )
        return make_piechart_author(properties_group)

    return update_piechart_author


def create_update_table_data_function(group):
    def update_table_data(
        figure, material_filter, isotope_filter, author_filter, year_filter
    ):
        data = []

        properties_group = group_to_make[group](
            materials=material_filter,
            authors=author_filter,
            isotopes=isotope_filter,
            years=year_filter,
        )

        for prop in properties_group:
            entry = {}
            for key in TABLE_KEYS:
                if hasattr(prop, key):
                    val = getattr(prop, key)
                    if key == "range":
                        if val is None:
                            val = "none"
                        else:
                            val = f"{val[0]:.0f}-{val[1]:.0f}"
                    elif key == "pre_exp" and hasattr(prop, "units"):
                        val = f"{val: .2e} {prop.units}"
                    elif key == "act_energy":
                        val = f"{val:.2f}"
                    entry[key] = val
                elif key == "doi":
                    entry[key] = prop.source
                    if prop.bibsource:
                        if "doi" in prop.bibsource.fields:
                            entry[
                                key
                            ] = f"[{prop.bibsource.fields['doi']}](https://doi.org/{prop.bibsource.fields['doi']})"
            data.append(entry)

        return data

    return update_table_data
