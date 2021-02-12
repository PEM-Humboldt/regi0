"""
Functions using the IUCN API.
"""
from typing import Union
from urllib.parse import urljoin

import pandas as pd
import requests

from ..utils import expand_result

API_URL = "https://apiv3.iucnredlist.org/api/v3/"


def _parse_response(response: requests.Response) -> dict:
    """

    Parameters
    ----------
    response

    Returns
    -------

    """
    if response.json().get("result"):
        result = response.json()["result"][0]
    else:
        result = {}

    return result


def _request(url: str, token: str) -> requests.Response:
    """

    Parameters
    ----------
    url
    token

    Returns
    -------

    """
    try:
        response = requests.get(url, params={"token": token})
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling IUCN API. {err}")
    if "message" in response.json():
        msg = response.json()["message"]
        raise Exception(f"Something when wrong calling IUCN API. {msg}")

    return response


def get_species_info(
    names: Union[list, pd.Series, str],
    token: str,
    add_supplied_names: bool = False,
    add_source: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """

    Parameters
    ----------
    names
    token
    add_supplied_names
    add_source
    expand

    Returns
    -------

    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)

    df = pd.DataFrame()
    endpoint = urljoin(API_URL, "species/")

    unique_names = pd.Series(names.dropna().unique())
    for name in unique_names:
        response = _request(urljoin(endpoint, name), token)
        if response.json().get("result"):
            result = pd.Series(response.json()["result"][0])
        else:
            result = pd.Series([], dtype="object")
        df = df.append(pd.Series(result), ignore_index=True)

    if add_supplied_names:
        df["supplied_name"] = unique_names
    if add_source:
        df["source"] = "IUCN"
    if expand:
        df = expand_result(names, df)


def get_country_occurrence(
    names: pd.Series,
    token: str,
    add_supplied_names: bool = False,
    add_source: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """

    Parameters
    ----------
    names
    token
    add_supplied_names
    add_source
    expand

    Returns
    -------

    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)

    df = pd.DataFrame()
    endpoint = urljoin(API_URL, "species/countries/name/")

    unique_names = pd.Series(names.dropna().unique())
    for name in unique_names:
        response = _request(urljoin(endpoint, name), token)
        if response.json().get("result"):
            temp_df = pd.DataFrame(response.json()["result"])
            result = pd.Series({
                field: values for field, values in zip(temp_df.columns, temp_df.T.values)
            })
        else:
            result = pd.Series([], dtype="object")
        df = df.append(pd.Series(result), ignore_index=True)

    if add_supplied_names:
        df["supplied_name"] = unique_names
    if add_source:
        df["source"] = "IUCN"
    if expand:
        df = expand_result(names, df)

    return df

