"""
General verification functions.
"""
import pandas as pd
from rapidfuzz import fuzz

from bdcctools.utils import standardize_text


def match(
    left: pd.Series,
    right: pd.Series,
    preprocess: bool = False,
    fuzzy: bool = False,
    threshold: float = 0.8,
) -> pd.Series:
    """

    Parameters
    ----------
    left
    right
    preprocess
    fuzzy
    threshold

    Returns
    -------

    """
    if preprocess:
        left = standardize_text(left)
        right = standardize_text(right)

    if fuzzy:
        values = pd.DataFrame({"left": left, "right": right})
        score = values.apply(lambda row: fuzz.ratio(row["left"], row["right"]), axis=1)
        result = (score / 100) >= threshold
    else:
        result = left == right

    return result


def verify(
    df: pd.DataFrame,
    observed_col: str,
    expected: pd.Series,
    flag_name: str,
    add_suggested: bool = False,
    suggested_name: str = None,
    drop: bool = False,
    **kwargs
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
    add_suggested:  Whether to add a column to the result with suggested
                    values for those rows where the observed values do not
                    match the expected values.
    suggested_name: Name of the column for the suggested values. Only has
                    effect when add_suggested=True is passed.
    drop:           Whether to drop the rows where the observed values
                    do not match the expected values.
    kwargs:         Keyword arguments accepted by the match function.

    Returns
    -------
    Copy of `df` with extra columns.
    """
    df = df.copy()

    df[flag_name] = match(df[observed_col], expected, **kwargs)

    if add_suggested:
        df.loc[~df[flag_name], suggested_name] = expected.loc[~df[flag_name]]
    if drop:
        df = df[~df[flag_name]]

    return df
