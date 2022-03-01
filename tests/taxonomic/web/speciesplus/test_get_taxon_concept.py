"""
Test cases for the regi0.taxonomic.web.gnr.resolve function.
"""
import numpy as np
import pandas as pd
import pytest

from regi0.taxonomic.web.speciesplus import get_taxon_concept


def test_success(success):
    result = get_taxon_concept(
        "Herpailurus yagouaroundi",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_names=True,
    )
    expected = pd.DataFrame(
        {
            "id": [98337],
            "author_year": ["(É. Geoffroy Saint-Hilaire, 1803)"],
            "cites_listing": ["I/II"],
            "common_names": ["Jaguarundi|Eyra Cat|Texas Jaguarundi"],
            "synonyms": [
                "Herpailurus yaguarondi|Felis yaguarondi|Herpailurus yagouaroundi|Puma yagouaroundi"
            ],
            "class": ["Mammalia"],
            "family": ["Felidae"],
            "kingdom": ["Animalia"],
            "order": ["Carnivora"],
            "phylum": ["Chordata"],
            "supplied_name": ["Herpailurus yagouaroundi"],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_no_result(no_result):
    result = get_taxon_concept(
        "Ceroxylon sasaimae",
        token="bsgkp2kagTzJdQuywXnefAbc",
    )
    expected = pd.DataFrame(
        {
            "id": [np.nan],
            "author_year": [np.nan],
            "cites_listing": [np.nan],
            "common_names": [np.nan],
            "synonyms": [np.nan],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_unauthorized(unauthorized):
    with pytest.raises(Exception):
        get_taxon_concept("Herpailurus yagouaroundi", token="csgkp2kagTzJdQuywXnefAbz")
