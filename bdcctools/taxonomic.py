"""
Functions for taxonomic verifications.
"""
import pandas as pd


def verify(values: pd.Series, other: pd.Series) -> pd.DataFrame:
    """

    Parameters
    ----------
    values
    other

    Returns
    -------

    """
    pass


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
