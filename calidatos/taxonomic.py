"""
Functions for taxonomic verifications.
"""
import numpy as np
import pandas as pd
import requests
from calidatos.utils import gnr_resolve


def check_species(
    df: pd.DataFrame,
    species_col: str,
    flag_name: str,
    add_suggested: bool = False,
    suggested_name: str = None,
    add_source: bool = False,
    source_name: str = None,
    drop: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Checks that the scientific names of records are valid using the
    Global Names Resolver API.

    Parameters
    ----------
    df:             DataFrame with records.
    species_col:    Column name with the species name for each record.
    flag_name:      Column name for the flag.
    add_suggested:  Whether to add suggested names for records where the
                    flag is True.
    suggested_name: Column name for the suggestion if values do not match.
    add_source:     Whether to add the verification source for all the
                    records.
    source_name:    Name for the source column.
    drop:           Whether to drop records where the flag is True.
    kwargs:         Keyword arguments passed to the gnr_resolve function.

    Returns
    -------
    Copy of original DataFrame or a subset (if drop is True) with extra
    columns.
    """
    # Make sure to modify a copy of the original DataFrame instead of
    # modifying it in place.
    df = df.copy()

    # Regardless of the value passed for `best_match_only` in kwargs,
    # its value is forced to be True so that only one result per
    # species is returned.
    kwargs.update({"best_match_only": True})

    unique_species = df[species_col].dropna().unique()
    result = gnr_resolve(unique_species, **kwargs)

    column_subset = ["data_source_title", "canonical_form", "supplied_name_string"]
    df = pd.merge(
        df,
        result[column_subset],
        how="left",
        left_on=species_col,
        right_on="supplied_name_string",
    )

    # Check whether the canonical form retrieved from GNR is complete
    # (i.e. has both genus and epithet). This is done by making sure
    # that the resulting canonical form has two words (first word
    # corresponding to genus and second to epithet). GNR retrieves just
    # the genus when it cannot resolve the complete name. For example,
    # passing Sterculia sp. will yield only Sterculia as a canonical form.
    is_complete = df["canonical_form"].str.split().str.len() == 2

    names_match = df["supplied_name_string"] == df["canonical_form"]
    df[flag_name] = names_match & is_complete
    if add_suggested:
        mask = ~names_match & is_complete
        df.loc[mask, suggested_name] = df.loc[mask, "canonical_form"]
    if add_source:
        df[source_name] = df["data_source_title"]
    if drop:
        df = df[df[flag_name]]

    df = df.drop(columns=column_subset)

    return df


def get_authority(names: pd.Series, token: str) -> pd.Series:
    """
    Gets the authority for different scientific names using the IUCN API.

    Parameters
    ----------
    names: Scientific names to get risk categories for.
    token: IUCN API token.

    Returns
    -------
    Series with the corresponding authorities.
    """
    return get_iucn_info(names, token, fields=["authority"])


def get_cites_listing(names: pd.Series, token: str) -> pd.Series:
    """
    Gets the corresponding cites listing for a set of scientific names.

    Parameters
    ----------
    names: Scientific names to get cites listings for.
    token: Species+ API token.

    Returns
    -------
    Series with the corresponding cites listings.
    """
    api_url = "https://api.speciesplus.net/api/v1/taxon_concepts"
    headers = {"X-Authentication-Token": token}

    result = pd.Series([None] * names.size, name="cites_listing", dtype="object")

    for name in names.dropna().unique():
        try:
            response = requests.get(api_url, params={"name": name}, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f"Error calling Species+ API. {err}")
        if response.json()["taxon_concepts"]:
            result[names == name] = response.json()["taxon_concepts"][0][
                "cites_listing"
            ]

    return result


def get_classification(
    names: pd.Series,
    return_unique: bool = False,
    add_supplied_names: bool = False,
    add_source: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """

    Parameters
    ----------
    names
    return_unique
    add_supplied_names
    add_source

    Returns
    -------

    """
    # Regardless of the value passed for `best_match_only` in kwargs,
    # its value is forced to be True so that only one result per
    # species is returned.
    kwargs.update({"best_match_only": True})
    unique_species = pd.Series(names.dropna().unique())
    result = gnr_resolve(unique_species, **kwargs)

    ranks = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    classification = pd.DataFrame(columns=ranks, index=unique_species.index)
    rank_indices = result["classification_path_ranks"].str.split("|", expand=True)
    path_indices = result["classification_path"].str.split("|", expand=True)

    for rank in ranks:
        mask = (rank_indices == rank).any(axis=1)
        rank_idx = np.nonzero(rank_indices[mask].values == rank)
        rank_paths = path_indices.values[rank_idx]
        classification.loc[mask, rank] = rank_paths

    if add_supplied_names:
        classification["supplied_name"] = unique_species

    if add_source:
        classification["source"] = result["data_source_title"]

    if not return_unique:
        if not names.name:
            names.name = "__supplied_name"
        classification["name"] = unique_species
        classification = pd.merge(
            names, classification, left_on=names.name, right_on="name"
        )
        classification = classification.drop(columns=[names.name, "name"])

    return classification


def get_elevation_range(names: pd.Series, token: str) -> pd.Series:
    """
    Gets the elevation range for different species using the IUCN API.

    Parameters
    ----------
    names: Scientific names to get risk categories for.
    token: IUCN API token.

    Returns
    -------
    Series with the corresponding authorities.
    """
    return get_iucn_info(names, token, fields=["elevation_lower", "elevation_upper"])


def get_iucn_info(names: pd.Series, token: str, fields: list = None) -> pd.DataFrame:
    """

    Parameters
    ----------
    names
    token
    fields

    Returns
    -------

    """
    api_url = "https://apiv3.iucnredlist.org/api/v3/species"

    iucn_info = pd.DataFrame()

    for name in names.dropna().unique():
        try:
            species_url = f"{api_url}/{name}"
            response = requests.get(species_url, params={"token": token})
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f"Error calling IUCN API. {err}")
        if "message" in response.json():
            msg = response.json()["message"]
            raise Exception(f"Something when wrong calling IUCN API. {msg}")

        if response.json().get("result"):
            result = response.json()["result"][0]
            species_info = pd.Series(result)
        else:
            species_info = pd.Series([], dtype="object")
        iucn_info = iucn_info.append(species_info, ignore_index=True)

    if fields:
        iucn_info = iucn_info[fields]

    return iucn_info


def get_iucn_species_id(names: pd.Series, token: str) -> pd.Series:
    """
    Gets the IUCN species ID for different species.

    Parameters
    ----------
    names: Scientific names to get risk categories for.
    token: IUCN API token.

    Returns
    -------
    Series with the corresponding IUCN species ID.
    """
    return get_iucn_info(names, token, fields=["taxonid"])


def get_risk_category(names: pd.Series, token: str) -> pd.Series:
    """
    Gets the global risk category assigned to the species according to
    the IUCN.

    Parameters
    ----------
    names: Scientific names to get risk categories for.
    token: IUCN API token.

    Returns
    -------
    Series with the corresponding risk categories.
    """
    return get_iucn_info(names, token, fields=["category"])


def get_species_countries(
    names: pd.Series,
    token: str,
    return_unique: bool = False,
    field: str = "code",
    delimiter: str = "|",
) -> pd.Series:
    """

    Parameters
    ----------
    names
    token
    return_unique
    field
    delimiter

    Returns
    -------

    """
    api_url = "https://apiv3.iucnredlist.org/api/v3/species/countries/name"

    if return_unique:
        index = None
    else:
        index = names.index
    result = pd.Series(index=index, dtype="object", name="countries")

    for name in names.dropna().unique():
        try:
            species_url = f"{api_url}/{name}"
            response = requests.get(species_url, params={"token": token})
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f"Error calling IUCN API. {err}")
        if "message" in response.json():
            msg = response.json()["message"]
            raise Exception(f"Something when wrong calling IUCN API. {msg}")

        if return_unique:
            names_index = len(result)
        else:
            names_index = names[names == name].index

        if response.json().get("result"):
            countries = map(lambda x: x.get(field), response.json()["result"])
            result.loc[names_index] = delimiter.join(countries)
        else:
            result.loc[names_index] = None

    return result
