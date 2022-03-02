"""
Test cases for the regi0.taxonomic.web.gnr.get_classification function.
"""
import numpy as np
import pandas as pd
import pytest

from regi0.taxonomic.web.gnr import get_classification


def test_success(success):
    result = get_classification(
        ["Panthera onca", "Tremarctos ornatus"],
        data_source_ids=["1"],
        add_supplied_names=True,
        add_source=True,
        expand=False,
    )
    expected = pd.DataFrame(
        {
            "kingdom": ["Animalia", "Animalia"],
            "phylum": ["Chordata", "Chordata"],
            "class": ["Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora"],
            "family": ["Felidae", "Ursidae"],
            "genus": ["Panthera", "Tremarctos"],
            "species": ["Panthera onca", "Tremarctos ornatus"],
            "supplied_name": ["Panthera onca", "Tremarctos ornatus"],
            "source": ["Catalogue of Life Checklist", "Catalogue of Life Checklist"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = get_classification(
        ["Ceroxylon sasaimae"],
        data_source_ids=["5"],
        add_supplied_names=True,
        add_source=True,
        expand=False,
    )
    expected = pd.DataFrame(
        {
            "kingdom": [np.nan],
            "phylum": [np.nan],
            "class": [np.nan],
            "order": [np.nan],
            "family": [np.nan],
            "genus": [np.nan],
            "species": [np.nan],
            "supplied_name": ["Ceroxylon sasaimae"],
            "source": [np.nan],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_bad_request(bad_request):
    with pytest.raises(Exception):
        get_classification(
            ["Panthera onca", "Tremarctos ornatus"], data_source_ids=["1"], expand=False
        )
