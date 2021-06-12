"""
Functions for local taxonomic verifications.
"""
import pathlib
from typing import Union

import pandas as pd


from bdcctools.io import read_table


def get_checklist_fields(
    names: Union[list, pd.Series, str],
    checklist: pd.DataFrame,
    name_field: str,
    fields: Union[list, str],
    add_supplied_names: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """
    Retrieves values for one or multiple fields from a checklist given
    some species names.

    Parameters
    ----------
    names:              Pandas Series with species names.
    checklist:          Pandas DataFrame wih checklist information.
    name_field:         Name of the column in `checklist` with species
                        names.
    fields:             List of fields (columns) to retrieve from
                        `checklist`.
    add_supplied_names: Whether to add `names` as an extra column in the
                        result.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`.

    Returns
    -------
    Pandas DataFrame with the values retrieved from `checklist`.
    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)
    names.name = "supplied_name"
    if isinstance(fields, str):
        fields = [fields]

    result = pd.merge(
        names, checklist, how="left", left_on="supplied_name", right_on=name_field
    )
    present_fields = list(set(fields).intersection(checklist.columns))
    absent_fields = list(set(fields).difference(checklist.columns))
    result = result[present_fields + ["supplied_name"]]
    result[absent_fields] = pd.NA
    result = result[fields + ["supplied_name"]]

    if not expand:
        result = result.drop_duplicates("supplied_name", ignore_index=True)
    if not add_supplied_names:
        result = result.drop(columns="supplied_name")

    return result


def get_checklist_fields_multiple(
    names: Union[list, pd.Series, str],
    filenames: list,
    name_field: str,
    fields: Union[list, str],
    add_supplied_names: bool = False,
    expand: bool = True,
    keep_first: bool = True,
    add_source: bool = False,
    source_name: str = "source"
) -> pd.DataFrame:
    """
    Retrieves values for one or multiple fields from multiple checklists
    given some species names. If a species name is found on more than one
    checklist, only the field(s) values for one of them is kept.

    Parameters
    ----------
    names:              Pandas Series with species names.
    filenames:          List of checklist file names.
    name_field:         Name of the column in `checklist` with species
                        names.
    fields:             List of fields (columns) to retrieve from
                        `checklist`.
    add_supplied_names: Whether to add `names` as an extra column in the
                        result.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`.
    keep_first:         Whether to keep the first match from a checklist
                        or use the latest.
    add_source:         Whether to add the checklist name where the values
                        were retrieved from.
    source_name:        Name of the column with the source.

    Returns
    -------
    Pandas DataFrame with the values retrieved from the checklists.
    """
    result = None
    for fn in filenames:
        checklist = read_table(fn)
        temp_result = get_checklist_fields(
            names, checklist, name_field, fields, add_supplied_names, expand
        )
        mask = temp_result[fields].notna().any(axis=1)
        if add_source:
            stem = pathlib.Path(fn).stem
            temp_result.loc[mask, source_name] = stem
        if result is None:
            result = temp_result
        else:
            if keep_first:
                mask = result[fields].isna().all(axis=1) & mask
            result[mask] = temp_result[mask]

    return result


def is_in_checklist(
    names: Union[list, pd.Series, str],
    checklist: pd.DataFrame,
    name_field: str,
    add_supplied_names: bool = False,
    expand: bool = True
) -> pd.DataFrame:
    """
    Checks whether some species names are found in a given checklist.

    Parameters
    ----------
    names:              Pandas Series with species names.
    checklist:          Pandas DataFrame wih checklist information.
    name_field:         Name of the column in `checklist` with species
                        names.
    add_supplied_names: Whether to add `names` as an extra column in the
                        result.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`.

    Returns
    -------
    Pandas DataFrame with a Boolean Series indicating whether `names` are
    present in `checklist`. If add_supplied_names=True is passed, the
    result will have an extra column.
    """
    if isinstance(names, (list, str)):
        names = pd.Series(names)
    names.name = "supplied_name"

    if not expand:
        names = names.drop_duplicates().dropna().reset_index(drop=True)
    result = names.isin(checklist[name_field])
    result.name = "in_checklist"

    result.loc[names.isna()] = pd.NA

    if add_supplied_names:
        result = pd.concat([result, names], axis=1)

    if isinstance(result, pd.Series):
        result = pd.DataFrame(result)

    return result


def is_in_checklist_multiple(
    names: Union[list, pd.Series, str],
    filenames: list,
    name_field: str,
    add_supplied_names: bool = False,
    expand: bool = True,
    keep_first: bool = True,
    add_source: bool = False,
    source_name: str = "source"
) -> Union[pd.DataFrame, pd.Series]:
    """
    Checks whether some species names are found in a multiple checklist.

    Parameters
    ----------
    names:              Pandas Series with species names.
    filenames:          List of checklist file names.
    name_field:         Name of the column in `checklist` with species
                        names.
    add_supplied_names: Whether to add `names` as an extra column in the
                        result.
    expand:             Whether to expand result rows to match `names`
                        size. If False, the number of rows will correspond
                        to the number of unique names in `names`.
    keep_first:         Whether to keep the first match from a checklist
                        or use the latest.
    add_source:         Whether to add the checklist name where the values
                        were retrieved from.
    source_name:        Name of the column with the source.

    Returns
    -------
    Pandas DataFrame with a Boolean Series indicating whether `names` are
    present in the checklists. If add_supplied_names=True or
    add_source=True, the result will have extra columns.
    """
    result = None
    for fn in filenames:
        checklist = read_table(fn)
        temp_result = is_in_checklist(
            names, checklist, name_field, add_supplied_names, expand
        )
        mask = temp_result["in_checklist"].fillna(False)
        if add_source:
            stem = pathlib.Path(fn).stem
            temp_result.loc[mask, source_name] = stem
        if result is None:
            result = temp_result
        else:
            if keep_first:
                mask = ~result["in_checklist"].fillna(False) & mask
            result[mask] = temp_result[mask]

    return result
