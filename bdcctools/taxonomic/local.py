"""
Functions for local taxonomic verifications.
"""
from typing import Union

import pandas as pd


def get_checklist_fields(
    names: Union[list, pd.Series, str],
    checklist: pd.DataFrame,
    name_field: str,
    fields: Union[list, str],
    add_supplied_names: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """

    Parameters
    ----------
    names
    checklist
    name_field
    fields
    add_supplied_names
    expand

    Returns
    -------

    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)
    names.name = "supplied_name"
    if isinstance(fields, str):
        fields = [fields]

    df = pd.merge(
        names, checklist, how="left", left_on="supplied_name", right_on=name_field
    )
    df = df[fields + ["supplied_name"]]

    if not expand:
        df = df.drop_duplicates("supplied_name", ignore_index=True)
    if not add_supplied_names:
        df = df.drop(columns="supplied_name")

    return df


def is_in_checklist(
    names: Union[list, pd.Series, str],
    checklist: pd.DataFrame,
    name_field: str,
    add_supplied_names: bool = False,
    expand: bool = True
) -> Union[pd.DataFrame, pd.Series]:
    """

    Parameters
    ----------
    names
    checklist
    name_field
    add_supplied_names
    expand

    Returns
    -------

    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)
    names.name = "supplied_name"

    if not expand:
        names = names.drop_duplicates().dropna().reset_index(drop=True)
    result = names.isin(checklist[name_field])
    result.name = "in_checklist"

    if add_supplied_names:
        result = pd.concat([result, names], axis=1)

    return result
