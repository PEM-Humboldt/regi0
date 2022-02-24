"""
Test cases for the regi0.taxonomic.web.gnr.get_classification function.
"""
import pandas as pd
import pytest

from regi0.taxonomic.web.gnr import get_classification


def test_defaults(success):
    result = get_classification(
        ["Panthera onca", "Tremarctos ornatus"], data_source_ids=["1"]
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
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_supplied_name(success):
    result = get_classification(
        ["Panthera onca", "Tremarctos ornatus"],
        data_source_ids=["1"],
        add_supplied_names=True,
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
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_source(success):
    result = get_classification(
        ["Panthera onca", "Tremarctos ornatus"],
        data_source_ids=["1"],
        add_source=True,
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
            "source": ["Catalogue of Life Checklist", "Catalogue of Life Checklist"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_bad_request(bad_request):
    with pytest.raises(Exception):
        get_classification(
            ["Panthera onca", "Tremarctos ornatus"], data_source_ids=["1"]
        )
