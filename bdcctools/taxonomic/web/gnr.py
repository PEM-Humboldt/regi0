"""
Wrappers for GNR API calls and derived functions.

API documentation can be found at: http://resolver.globalnames.org/api
"""
from typing import Union

import numpy as np
import pandas as pd
import requests

from bdcctools.taxonomic.utils import expand_result

API_URL = "http://resolver.globalnames.org/name_resolvers.json"


def resolve(
    names: Union[list, pd.Series, str],
    data_source_ids: list = None,
    resolve_once: bool = False,
    best_match_only: bool = False,
    with_context: bool = False,
    with_vernaculars: bool = False,
    with_canonical_ranks: bool = False
) -> pd.DataFrame:
    """
    Receives a list of names and resolves each against the entire resolver
    database or against specific data sources using the Global Names
    Resolver (GNR) API. Underlying resolving and scoring algorithms are
    described at: http://resolver.globalnames.org/about

    Parameters
    ----------
    names:                  List of species names to resolve.
    data_source_ids:        List of specific data sources IDs to resolve
                            against. A list of all the available data
                            sources and their IDs can be found at:
                            http://resolver.globalnames.org/data_sources.
    resolve_once:           Find the first available match instead of
                            matches across all data sources with all
                            possible renderings of a name.
    best_match_only:        Returns just one result with the highest
                            score.
    with_context:           Reduce the likelihood of matches to taxonomic
                            homonyms. When True, a common taxonomic
                            context is calculated for all supplied names
                            from matches in data sources that have
                            classification tree paths. Names out of
                            determined context are penalized during
                            score calculation.
    with_vernaculars:       Return 'vernacular' field to present common
                            names provided by a data source for a
                            particular match.
    with_canonical_ranks:   Returns 'canonical_form' with infraspecific
                            ranks, if they are present.

    Returns
    -------
    List with the results for each name in names.

    Notes
    -----
    More information on the GNR API can be found at:
    http://resolver.globalnames.org/api
    """
    if isinstance(names, str):
        names = [names]
    if data_source_ids is None:
        data_source_ids = []

    # Apparently, GNR API does not accept Booleans so they need to be
    # converted to lowercase strings first.
    params = {
        "data": "\n".join(names),
        "data_source_ids": "|".join(data_source_ids),
        "resolve_once": str(resolve_once).lower(),
        "best_match_only": str(best_match_only).lower(),
        "with_context": str(with_context).lower(),
        "with_vernaculars": str(with_vernaculars).lower(),
        "with_canonical_ranks": str(with_canonical_ranks).lower()
    }

    try:
        response = requests.post(API_URL, json=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling Global Name Resolver API. {err}")

    data = response.json()["data"]

    return pd.json_normalize(data, record_path="results", meta="supplied_name_string")


def get_classification(
    names: Union[list, pd.Series, str],
    add_supplied_names: bool = False,
    add_source: bool = False,
    expand: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Gets the complete classification of multiple scientific names using
    the Global Names Resolver.

    Parameters
    ----------
    names:              Scientific name(s) to get results for.
    add_supplied_names: Add supplied scientific names column to the
                        resulting DataFrame.
    add_source:         Add source column to the resulting DataFrame.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`. Only
                        has effect if best_match_only=True is passed.
    kwargs:             Keyword arguments of the resolve function.

    Returns
    -------
    Classification DataFrame.
    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)

    unique_names = pd.Series(names.dropna().unique())
    result = resolve(unique_names, **kwargs)

    ranks = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    df = pd.DataFrame(columns=ranks, index=result.index)
    rank_indices = result["classification_path_ranks"].str.split("|", expand=True)
    path_indices = result["classification_path"].str.split("|", expand=True)

    for rank in ranks:
        mask = (rank_indices == rank).any(axis=1)
        rank_idx = np.nonzero(rank_indices[mask].values == rank)
        rank_paths = path_indices[mask].values[rank_idx]
        df.loc[mask, rank] = rank_paths

    if add_supplied_names:
        df["supplied_name"] = unique_names
    if add_source:
        df["source"] = result["data_source_title"]
    if kwargs.get("best_match_only"):
        if expand:
            df = expand_result(df, names)

    return df
