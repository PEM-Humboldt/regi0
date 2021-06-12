"""
Wrappers for Species+/CITES checklist API calls.

API documentation can be found at: http://api.speciesplus.net/documentation
"""
from typing import Union
from urllib.parse import urljoin

import pandas as pd
import requests

from bdcctools.taxonomic.utils import expand_result

API_URL = "https://api.speciesplus.net/api/v1/"


def _request(url: str, token: str, params: dict) -> requests.Response:
    """
    Creates a request for the Species+/CITES checklist API and handles
    HTTP exceptions.

    Parameters
    ----------
    url:     Species+/CITES checklist API endpoint.
    token:   Species+/CITES checklist API authentication token.
    params:  Request parameters.

    Returns
    -------
    Request response.
    """
    headers = {"X-Authentication-Token": token}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling Species+ API. {err}")

    return response


def get_taxon_concepts(
    names: Union[list, pd.Series, str],
    token: str,
    add_supplied_names: bool = False,
    add_source: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """
    Calls the taxon_concepts endpoint of the Species+/CITES checklist API
    for multiple scientific names.

    Parameters
    ----------
    names:              Scientific name(s) to get results for.
    token:              Species+/CITES checklist API authentication token.
    add_supplied_names: Add supplied scientific names column to the
                        resulting DataFrame.
    add_source:         Add source column to the resulting DataFrame.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`.

    Returns
    -------
    Series with the corresponding cites listings.
    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)

    endpoint = urljoin(API_URL, "taxon_concepts")
    df = pd.DataFrame()

    unique_names = names.dropna().unique()
    for name in unique_names:
        response = _request(endpoint, token, {"name": name})
        if response.json().get("taxon_concepts"):
            result = pd.DataFrame(response.json()["taxon_concepts"])
        else:
            result = pd.Series([], dtype="object")
        df = df.append(result, ignore_index=True)

    if add_supplied_names:
        df["supplied_name"] = unique_names
    if add_source:
        df["source"] = "Species+/CITES"
    if expand:
        df = expand_result(df, names)

    return df
