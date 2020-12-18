"""
Functions for taxonomic verifications.
"""

import pandas as pd
from recovery.util import gnr_resolve


def check_species(
    df: pd.DataFrame,
    species_col: str,
    flag_name: str,
    add_suggested: bool = False,
    suggested_name: str = None,
    add_source: bool = False,
    source_name: str = None,
    drop: bool = False,
    **kwargs
) -> pd.DataFrame:
    """

    Parameters
    ----------
    df
    species_col
    flag_name
    add_suggested:
    suggested_name:
    add_source
    source_name
    drop
    kwargs:         Keyword arguments passed to the gnr_resolve function.

    Returns
    -------

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
        right_on="supplied_name_string"
    )

    # Check whether the canonical form retrieved from GNR is complete
    # (i.e. has both genus and epithet). This is done by making sure
    # that the resulting canonical form has two words (first word
    # corresponding to genus and second to epithet). GNR retrieves just
    # the genus when it cannot resolve the complete name. For example,
    # passing Sterculia sp. will yield only Sterculia as a canonical form.
    is_complete = df["canonical_form"].str.split().str.len() == 2

    df[flag_name] = (df["supplied_name_string"] == df["canonical_form"]) & is_complete
    if add_suggested:
        df.loc[~df[flag_name], suggested_name] = df.loc[~df[flag_name], "canonical_form"]
    if add_source:
        df[source_name] = df["data_source_title"]
    if drop:
        df = df[df[flag_name]]

    df = df.drop(columns=column_subset)

    return df


# TODO: scientificNameAuthorship: check if it is possible to get from GNR or Taxize.
# TODO: taxonomicStatus: Check if it is possible to get from GNR or Taxize.
