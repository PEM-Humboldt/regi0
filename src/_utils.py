import pandas as pd


def _get_most_recent_year(
    dates: pd.Series, unique_years: list, round_unmatched=False
) -> pd.Series:
    """

    Parameters
    ----------
    dates
    unique_years
    round_unmatched

    Returns
    -------

    Notes
    -----
    This function is based on the answer given on:
    https://stackoverflow.com/a/64881346/7144368
    """
    years = pd.to_datetime(dates).dt.year
    years = years.sort_values()

    dummy_df = pd.DataFrame({years.name: unique_years, "__year": unique_years})
    result = pd.merge_asof(years, dummy_df, on=years.name)["__year"]

    if round_unmatched:
        result[result.isna()] = min(unique_years)

    result.index = years.index
    result = result.sort_index()

    return result.astype(int)
