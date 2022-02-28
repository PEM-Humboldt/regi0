"""
Wrappers for Species+/CITES checklist API calls.

API documentation can be found at: http://api.speciesplus.net/documentation
"""
from typing import Union
from urllib.parse import urljoin

import pandas as pd
import requests

from .._helpers import expand_result

API_URL = "https://api.speciesplus.net/api/v1/"


def _request(url: str, token: str, params: dict) -> requests.Response:
    """
    Creates a request for the Species+/CITES checklist API and handles
    HTTP exceptions.

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
    requests.Response
        Request response.

    """
    headers = {"X-Authentication-Token": token}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling Species+ API. {err}")

    return response


def get_taxon_concept(
    names: Union[list, pd.Series, str],
    token: str,
    expand: bool = True,
    language: Union[str, list] = "EN",
) -> pd.Series:
    """
    Get the most recent taxon concept for multiple scientific names using
    the taxon_concepts endpoint of the Species+/CITES checklist API.

    Parameters
    ----------
    names : list, Series or str
        Scientific name(s) to get results for.
    token : str
        Species+/CITES checklist API authentication token.
    expand : bool
        Whether to expand result rows to match `names` size. If False,
        the number of rows will correspond to the number of unique names
        in `names`.
    language : str or list
        One or multiple ISO 639-1 codes (codes for the representation of
        names of languages; e.g. EN or ES) used to filter languages
        returned for common names.

    Returns
    -------
    Series
        Series with taxon concept information.

    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)

    if isinstance(language, str):
        language = language

    endpoint = urljoin(API_URL, "taxon_concepts")

    df = pd.DataFrame()

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

    if expand:
        df = expand_result(df, names)

    return df
