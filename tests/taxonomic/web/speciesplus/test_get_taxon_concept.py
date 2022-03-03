"""
Test cases for the regi0.taxonomic.web.speciesplus.get_taxon_concept function.
"""
import numpy as np
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.speciesplus import get_taxon_concept


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "pagination": {"current_page": 1, "per_page": 500, "total_entries": 2},
            "taxon_concepts": [
                {
                    "id": 98337,
                    "full_name": "Herpailurus yagouaroundi",
                    "author_year": "(É. Geoffroy Saint-Hilaire, 1803)",
                    "rank": "SPECIES",
                    "name_status": "A",
                    "updated_at": "2020-02-07T10:35:58.886Z",
                    "active": True,
                    "cites_listing": "I/II",
                    "higher_taxa": {
                        "kingdom": "Animalia",
                        "phylum": "Chordata",
                        "class": "Mammalia",
                        "order": "Carnivora",
                        "family": "Felidae",
                    },
                    "synonyms": [
                        {
                            "id": 12288,
                            "full_name": "Puma yagouaroundi panamensis",
                            "author_year": "(J. A. Allen, 1904)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 33706,
                            "full_name": "Herpailurus yaguarondi",
                            "author_year": "(É. Geoffroy, Saint-Hilaire, 1803)",
                            "rank": "SPECIES",
                        },
                        {
                            "id": 98339,
                            "full_name": "Herpailurus yagouaroundi tolteca",
                            "author_year": "(Thomas, 1898)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 12164,
                            "full_name": "Puma yagouaroundi tolteca",
                            "author_year": "(Thomas, 1898)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 98342,
                            "full_name": "Herpailurus yagouaroundi panamensis",
                            "author_year": "(J. A. Allen, 1904)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 34660,
                            "full_name": "Felis yaguarondi",
                            "author_year": "É. Geoffroy Saint-Hilaire, 1803",
                            "rank": "SPECIES",
                        },
                        {
                            "id": 98340,
                            "full_name": "Herpailurus yagouaroundi fossata",
                            "author_year": "(Mearns, 1901)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 12334,
                            "full_name": "Puma yagouaroundi fossata",
                            "author_year": "(Mearns, 1901)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 98341,
                            "full_name": "Herpailurus yagouaroundi cacomitli",
                            "author_year": "(Berlandier, 1859)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 55198,
                            "full_name": "Herpailurus yagouaroundi",
                            "author_year": "(Lacépède, 1809)",
                            "rank": "SPECIES",
                        },
                        {
                            "id": 12157,
                            "full_name": "Puma yagouaroundi cacomitli",
                            "author_year": "(Berlandier, 1859)",
                            "rank": "SUBSPECIES",
                        },
                        {
                            "id": 9682,
                            "full_name": "Puma yagouaroundi",
                            "author_year": "(É. Geoffroy Saint-Hilaire, 1803)",
                            "rank": "SPECIES",
                        },
                    ],
                    "common_names": [
                        {"name": "Jaguarundi", "language": "EN"},
                        {"name": "Eyra Cat", "language": "EN"},
                        {"name": "Texas Jaguarundi", "language": "EN"},
                    ],
                    "cites_listings": [
                        {
                            "id": 1574,
                            "appendix": "I",
                            "annotation": "Only the populations of Central and North America; all other populations are included in Appendix II.Formerly listed as Puma yagouaroundi, which became a synonym of Herpailurus yagouaroundi in 2019, following taxonomic changes adopted at CoP18.",
                            "hash_annotation": None,
                            "effective_at": "1987-10-22",
                            "party": None,
                        },
                        {
                            "id": 1575,
                            "appendix": "II",
                            "annotation": "[FAMILY listing Felidae spp.] Included in Felidae spp. except the populations of Central and North America, which are included in Appendix\xa0I. Specimens of the domesticated form are not subject to the provisions of the Convention. Formerly listed as Puma yagouaroundi, which became a synonym of Herpailurus yagouaroundi in 2019, following taxonomic changes adopted at CoP18.",
                            "hash_annotation": None,
                            "effective_at": "1987-10-22",
                            "party": None,
                        },
                    ],
                },
                {
                    "id": 55198,
                    "full_name": "Herpailurus yagouaroundi",
                    "author_year": "(Lacépède, 1809)",
                    "rank": "SPECIES",
                    "name_status": "S",
                    "updated_at": "2014-01-06T15:19:27.665Z",
                    "active": True,
                    "accepted_names": [
                        {
                            "id": 98337,
                            "full_name": "Herpailurus yagouaroundi",
                            "author_year": "(É. Geoffroy Saint-Hilaire, 1803)",
                            "rank": "SPECIES",
                        }
                    ],
                },
            ],
        }


class NoResult(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "pagination": {"current_page": 1, "per_page": 500, "total_entries": 0},
            "taxon_concepts": [],
        }


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


@pytest.fixture()
def no_result(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: NoResult())


def test_success(success):
    result = get_taxon_concept(
        "Herpailurus yagouaroundi",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_names=True,
        expand=False,
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
        "Ceroxylon sasaimae", token="bsgkp2kagTzJdQuywXnefAbc", expand=False
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
    with pytest.raises(requests.HTTPError):
        get_taxon_concept(
            "Herpailurus yagouaroundi", token="csgkp2kagTzJdQuywXnefAbz", expand=False
        )
