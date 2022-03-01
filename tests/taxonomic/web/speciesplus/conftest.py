"""
Configuration file for the regi0.taxonomic.web.speciesplus module tests.
"""
import pytest
import requests


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


class Unauthorized(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 401


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


@pytest.fixture()
def no_result(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: NoResult())


@pytest.fixture()
def unauthorized(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Unauthorized())
