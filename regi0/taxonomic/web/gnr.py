"""
Wrappers for GNR API calls and derived functions.

API documentation can be found at: http://resolver.globalnames.org/api
"""
import warnings
from typing import Union

import numpy as np
import pandas as pd
import requests

from .._helpers import expand_result

API_URL = "http://resolver.globalnames.org/name_resolvers.json"


def resolve(
    names: Union[list, np.ndarray, pd.Series, str],
    data_source_ids: list = None,
    resolve_once: bool = False,
    best_match_only: bool = False,
    with_context: bool = False,
    with_vernaculars: bool = False,
    with_canonical_ranks: bool = False,
    expand: bool = True,
) -> pd.DataFrame:
    """
    Receives a list of names and resolves each against the entire resolver
    database or against specific data sources using the Global Names
    Resolver (GNR) API. Underlying resolving and scoring algorithms are
    described at: http://resolver.globalnames.org/about

    Parameters
    ----------
    names : list, array, Series or str
        Scientific name(s) to get results for.
    data_source_ids : list
        List of specific data sources IDs to resolve against. A list of
        all the available data sources and their IDs can be found at:
        http://resolver.globalnames.org/data_sources.
    resolve_once : bool
        Find the first available match instead of matches across all data
        sources with all possible renderings of a name.
    best_match_only : bool
        Returns just one result with the highest score.
    with_context : bool
        Reduce the likelihood of matches to taxonomic homonyms. When True,
        a common taxonomic context is calculated for all supplied names
        from matches in data sources that have classification tree paths.
        Names out of determined context are penalized during score
        calculation.
    with_vernaculars : bool
        Return 'vernacular' field to present common names provided by a
        data source for a particular match.
    with_canonical_ranks : bool
        Returns 'canonical_form' with infraspecific ranks, if they are
        present.
    expand : bool
        Whether to expand result rows to match `names` size. If False, the
        number of rows will correspond to the number of unique names in
        `names`. Only has effect if best_match_only=True or if only one
         data source id is passed.

    Returns
    -------
    DataFrame
        DataFrame where rows are the result for each match.

    """
    if isinstance(names, (list, str, np.ndarray)):
        names = pd.Series(names)
    if data_source_ids is None:
        data_source_ids = []

    unique_names = names.dropna().unique()

    # Apparently, the GNR API does not accept Booleans so they need to be
    # converted to lowercase strings first.
    params = {
        "data": "\n".join(unique_names),
        "data_source_ids": "|".join(data_source_ids),
        "resolve_once": str(resolve_once).lower(),
        "best_match_only": str(best_match_only).lower(),
        "with_context": str(with_context).lower(),
        "with_vernaculars": str(with_vernaculars).lower(),
        "with_canonical_ranks": str(with_canonical_ranks).lower(),
    }

    try:
        response = requests.post(API_URL, json=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling Global Name Resolver API. {err}")

    data = response.json()["data"]

    # The pd.json_normalize() function does not work when record_path
    # is not found in every single item inside the list of elements
    # passed. In some cases, the GNR API returns items without this key,
    # so it needs to be added (including an empty dictionary) before
    # normalizing the result. Furthermore, there are some cases where
    # the GNR API returns items with this key but the list contains just
    # a None value, which causes pd.json_normalize to fail as well.
    for item in data:
        if "results" not in item:
            item["results"] = [{}]
        else:
            if not all(item["results"]):
                item["results"] = [{}]

    df = pd.json_normalize(data, record_path="results", meta="supplied_name_string")

    if expand:
        if best_match_only:
            df = expand_result(df, names)
        else:
            warnings.warn(
                "Result will not be expanded because there might be multiple results for"
                " each species. Make sure best_match_only is True for the result to be "
                "expanded."
            )

    return df


def get_classification(
    names: Union[list, np.ndarray, pd.Series, str],
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
    names : list, array, Series or str
        Scientific name(s) to get results for.
    add_supplied_names : bool
        Add supplied scientific names to the resulting DataFrame.
    add_source : bool
        Add source column to the resulting DataFrame.
    expand : bool
        Whether to expand result rows to match `names` size. If False, the
        number of rows will correspond to the number of unique names in
        `names`. Only has effect if best_match_only=True or if only one
         data source id is passed.
    **kwargs
        Keyword arguments of the resolve function.

    Returns
    -------
    DataFrame
        DataFrame with the ranks for each match.

    """
    if isinstance(names, (list, str, np.ndarray)):
        names = pd.Series(names)

    result = resolve(names, expand=expand, **kwargs)
    ranks = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    df = pd.DataFrame(columns=ranks, index=result.index)

    if (
        "classification_path_ranks" in result.columns
        and "classification_path" in result.columns
    ):
        rank_indices = result["classification_path_ranks"].str.split("|", expand=True)
        path_indices = result["classification_path"].str.split("|", expand=True)

        for rank in ranks:
            # The GNR API result might have duplicated ranks for one or more
            # items. Thus, duplicated ranks are removed and only the value for
            # first the appearance is kept.
            rank_idx = np.nonzero(rank_indices.values == rank)
            unique_idx = np.unique(rank_idx[0], return_index=True)[1]
            new_idx = np.column_stack(rank_idx)[unique_idx]
            rank_idx = tuple(new_idx.T)
            rank_paths = path_indices.values[rank_idx]
            df.loc[(rank_indices == rank).any(axis=1), rank] = rank_paths

    if add_supplied_names:
        df["supplied_name"] = result.get("supplied_name_string")
    if add_source:
        df["source"] = result.get("data_source_title")

    df = df.replace(["", None], np.nan)

    return df
