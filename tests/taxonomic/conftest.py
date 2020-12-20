import os

import pandas as pd
import pytest

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture(scope="session")
def records():
    return pd.read_csv(os.path.join(DATA_FOLDER, "csv", "trees.csv"))


@pytest.fixture(scope="session")
def expected():
    return pd.read_csv(os.path.join(DATA_FOLDER, "csv", "expected.csv"))
