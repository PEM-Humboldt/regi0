"""
General verification functions.
"""
import pandas as pd
from rapidfuzz import fuzz

from bdcctools.utils import standardize_text


def verify(
    df: pd.DataFrame,
    observed_col: str,
    expected: pd.Series,
    flag_name: str,
    preprocess: bool = False,
    fuzzy: bool = False,
    threshold: float = 0.8,
    add_suggested: bool = False,
    suggested_name: str = None,
    drop: bool = False
) -> pd.DataFrame:
    """
    Verifies that the values in a specific column from `df` match some
    expected values.

    Parameters
    ----------
    df:             pandas DataFrame.
    observed_col:   Name of the column in `df` with the values to verify.
    expected:       pandas Series with expected values. Has to match `df`
                    length.
    flag_name:      Name of the resulting column indicating whether the
                    observed values match the expected values.
    preprocess:
    fuzzy:
    threshold:
    add_suggested:  Whether to add a column to the result with suggested
                    values for those rows where the observed values do not
                    match the expected values.
    suggested_name: Name of the column for the suggested values. Only has
                    effect when add_suggested=True is passed.
    drop:           Whether to drop the rows where the observed values
                    do not match the expected values.

    Returns
    -------
    Copy of `df` with extra columns.
    """
    df = df.copy()

    observed = df[observed_col].copy()
    if preprocess:
        observed = standardize_text(observed)
        expected = standardize_text(expected)

    if fuzzy:
        values = pd.DataFrame({"left": observed, "right": expected})
        score = values.apply(lambda row: fuzz.ratio(row["left"], row["right"]), axis=1)
        score /= 100
        match = score >= threshold
    else:
        match = observed == expected

    df[flag_name] = match

    if add_suggested:
        df.loc[~match, suggested_name] = expected.loc[~match]
    if drop:
        df = df[~match]

    return df
