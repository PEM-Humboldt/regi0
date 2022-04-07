"""
Wrappers for Species+/CITES checklist API calls.

API documentation can be found at: http://api.speciesplus.net/documentation
"""
from typing import Union
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import requests

from .._helpers import expand_result

API_URL = "https://api.speciesplus.net/api/v1/"


def _request(url: str, token: str, params: dict = None) -> requests.Response:
    """
    Creates a request for the Species+/CITES checklist API.

    Parameters
    ----------
    url : str
        Species+/CITES checklist API endpoint.
    token : str
        Species+/CITES checklist API authentication token.
    params : dict
        Request parameters.

    Returns
    -------
    Response
        Request response.

    """
    headers = {"X-Authentication-Token": token}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    return response


def get_distributions(
    ids: Union[float, int, list, pd.Series, str],
    token: str,
    language: str = "EN",
    add_supplied_ids: bool = False,
    expand: bool = True,
) -> pd.DataFrame:
    """
    Get species distributions (i.e. country occurrences) for multiple
    taxon concept IDs.

    Parameters
    ----------
    ids : float, int, list, pd.Series, str
        Taxon concept ID(s) to get results for. A convenient way of
        retrieving these IDs for one or multiple scientific names is
        using the get_taxon_concept function, which returns an id column.
    token : Species+/CITES checklist API authentication token.
        Species+/CITES checklist API authentication token.
    language : str
        Language for the names of distributions. Can be "EN", "ES" or "FR".
    add_supplied_ids : bool
        Add supplied taxon_concept_ids to the resulting DataFrame.
    expand : bool
        Whether to expand result rows to match `names` size. If False,
        the number of rows will correspond to the number of unique names
        in `names`.

    Returns
    -------
    DataFrame
        DataFrame with distributions information.

    """
    if isinstance(ids, (float, int, list, str)):
        ids = pd.Series(ids)

    df = pd.DataFrame()

    unique_ids = ids.dropna().unique()
    for _id in unique_ids:
        endpoint = urljoin(API_URL, f"taxon_concepts/{int(_id)}/distributions")
        try:
            response = _request(endpoint, token, {"language": language})
            temp_df = pd.DataFrame(response.json())
            temp_df = temp_df.drop(columns=["tags", "references"])
            temp_df = temp_df.astype(str)
            result = pd.Series(
                {
                    field: values
                    for field, values in zip(temp_df.columns, temp_df.T.values)
                }
            )
            result = result.str.join("|")
        except requests.HTTPError as err:
            if err.response.status_code == 500:
                result = pd.Series([], dtype="object")
            else:
                raise requests.HTTPError(err)

        df = df.append(pd.Series(result), ignore_index=True)

    if add_supplied_ids:
        df["supplied_id"] = unique_ids
    if expand:
        df = expand_result(df, ids)

    return df


def get_references(
    ids: Union[float, int, list, pd.Series, str],
    token: str,
    add_supplied_ids: bool = False,
    expand: bool = True,
) -> pd.DataFrame:
    """
    Get references for multiple taxon concept IDs.

    Parameters
    ----------
    ids : float, int, list, pd.Series, str
        Taxon concept ID(s) to get results for. A convenient way of
        retrieving these IDs for one or multiple scientific names is
        using the get_taxon_concept function, which returns an id column.
    token : Species+/CITES checklist API authentication token.
        Species+/CITES checklist API authentication token.
    add_supplied_ids : bool
        Add supplied taxon_concept_ids to the resulting DataFrame.
    expand : bool
        Whether to expand result rows to match `names` size. If False,
        the number of rows will correspond to the number of unique names
        in `names`.

    Returns
    -------
    DataFrame
        DataFrame with references information.

    """
    if isinstance(ids, (float, int, list, str)):
        ids = pd.Series(ids)

    df = pd.DataFrame()

    unique_ids = ids.dropna().unique()
    for _id in unique_ids:
        endpoint = urljoin(API_URL, f"taxon_concepts/{int(_id)}/references")
        try:
            response = _request(endpoint, token)
            temp_df = pd.DataFrame(response.json())
            temp_df = temp_df.astype(str)
            result = pd.Series(
                {
                    field: values
                    for field, values in zip(temp_df.columns, temp_df.T.values)
                }
            )
            result = result.str.join("|")
        except requests.HTTPError as err:
            if err.response.status_code == 500:
                result = pd.Series([], dtype="object")
            else:
                raise requests.HTTPError(err)

        df = df.append(pd.Series(result), ignore_index=True)

    if add_supplied_ids:
        df["supplied_id"] = unique_ids
    if expand:
        df = expand_result(df, ids)

    return df


def get_taxon_concept(
    names: Union[list, np.ndarray, pd.Series, str],
    token: str,
    language: Union[str, list] = "EN",
    add_supplied_names: bool = False,
    expand: bool = True,
) -> pd.DataFrame:
    """
    Get the most recent taxon concept for multiple scientific names using
    the taxon_concepts endpoint of the Species+/CITES checklist API.

    Parameters
    ----------
    names : list, array, Series or str
        Scientific name(s) to get results for.
    token : str
        Species+/CITES checklist API authentication token.
    language : str or list
        One or multiple ISO 639-1 codes (codes for the representation of
        names of languages; e.g. EN or ES) used to filter languages
        returned for common names.
    add_supplied_names : bool
        Add supplied scientific names to the resulting DataFrame.
    expand : bool
        Whether to expand result rows to match `names` size. If False,
        the number of rows will correspond to the number of unique names
        in `names`.

    Returns
    -------
    DataFrame
        DataFrame with taxon concept information.

    """
    if isinstance(names, (list, str, np.ndarray)):
        names = pd.Series(names)

    if isinstance(language, str):
        language = [language]

    endpoint = urljoin(API_URL, "taxon_concepts")

    df = pd.DataFrame(
        columns=["id", "author_year", "cites_listing", "common_names", "synonyms"]
    )

    unique_names = names.dropna().unique()
    for name in unique_names:
        result = pd.Series([], dtype="object")
        response = _request(
            endpoint, token, {"name": name, "language": ",".join(language)}
        )
        taxon_concepts = response.json()["taxon_concepts"]
        if taxon_concepts:
            taxon_concept = sorted(
                taxon_concepts, key=lambda x: x["updated_at"], reverse=True
            )[0]
            result.loc["id"] = taxon_concept.get("id")
            result.loc["author_year"] = taxon_concept.get("author_year")
            result.loc["cites_listing"] = taxon_concept.get("cites_listing")
            result.loc["common_names"] = "|".join(
                [item.get("name") for item in taxon_concept.get("common_names")]
            )
            result.loc["synonyms"] = "|".join(
                [
                    item.get("full_name")
                    for item in taxon_concept.get("synonyms")
                    if item.get("rank") == "SPECIES"
                ]
            )
            if taxon_concept.get("higher_taxa"):
                for rank, value in taxon_concept.get("higher_taxa").items():
                    result.loc[rank] = value

        df = df.append(result, ignore_index=True)

    if add_supplied_names:
        df["supplied_name"] = unique_names
    if expand:
        df = expand_result(df, names)

    return df
