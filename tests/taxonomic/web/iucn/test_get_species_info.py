"""
Test cases for the regi0.taxonomic.web.iucn.get_species_info function.
"""
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.iucn import get_species_info


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "name": "Alouatta seniculus",
            "result": [
                {
                    "taxonid": 198676562,
                    "scientific_name": "Alouatta seniculus",
                    "kingdom": "ANIMALIA",
                    "phylum": "CHORDATA",
                    "class": "MAMMALIA",
                    "order": "PRIMATES",
                    "family": "ATELIDAE",
                    "genus": "Alouatta",
                    "main_common_name": "Colombian Red Howler Monkey",
                    "authority": "(Linnaeus, 1766)",
                    "published_year": 2021,
                    "assessment_date": "2021-04-13",
                    "category": "LC",
                    "criteria": None,
                    "population_trend": "Decreasing",
                    "marine_system": False,
                    "freshwater_system": False,
                    "terrestrial_system": True,
                    "assessor": "Link, A., Palacios, E., Cortés-Ortiz, L., Stevenson, P.R., Cornejo, F.M., Mittermeier, R.A., Shanee, S., de la Torre, S., Boubli, J.P., Guzmán-Caro, D.C., Moscoso, P., Urbani, B. & Seyjagat, J.",
                    "reviewer": "Reuter, K.E.",
                    "aoo_km2": None,
                    "eoo_km2": None,
                    "elevation_upper": None,
                    "elevation_lower": None,
                    "depth_upper": None,
                    "depth_lower": None,
                    "errata_flag": None,
                    "errata_reason": None,
                    "amended_flag": None,
                    "amended_reason": None,
                }
            ],
        }


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


def test_success(success):
    result = get_species_info(
        "Alouatta seniculus", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame(
        {
            "taxonid": [198676562],
            "scientific_name": ["Alouatta seniculus"],
            "kingdom": ["ANIMALIA"],
            "phylum": ["CHORDATA"],
            "class": ["MAMMALIA"],
            "order": ["PRIMATES"],
            "family": ["ATELIDAE"],
            "genus": ["Alouatta"],
            "main_common_name": ["Colombian Red Howler Monkey"],
            "authority": ["(Linnaeus, 1766)"],
            "published_year": [2021.0],
            "assessment_date": ["2021-04-13"],
            "category": ["LC"],
            "criteria": [None],
            "population_trend": ["Decreasing"],
            "marine_system": [0.0],
            "freshwater_system": [0.0],
            "terrestrial_system": [1.0],
            "assessor": [
                "Link, A., Palacios, E., Cortés-Ortiz, L., Stevenson, P.R., Cornejo, F.M., Mittermeier, R.A., Shanee, S., de la Torre, S., Boubli, J.P., Guzmán-Caro, D.C., Moscoso, P., Urbani, B. & Seyjagat, J."
            ],
            "reviewer": ["Reuter, K.E."],
            "aoo_km2": [None],
            "eoo_km2": [None],
            "elevation_upper": [None],
            "elevation_lower": [None],
            "depth_upper": [None],
            "depth_lower": [None],
            "errata_flag": [None],
            "errata_reason": [None],
            "amended_flag": [None],
            "amended_reason": [None],
            "supplied_name": ["Alouatta seniculus"],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_no_result(no_result):
    result = get_species_info(
        "Ceroxylon sasaimae", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame({"supplied_name": ["Ceroxylon sasaimae"]})
    pd.testing.assert_frame_equal(result, expected)


def test_unauthorized(unauthorized):
    with pytest.raises(Exception):
        get_species_info("Alouatta seniculus", token="551f4z6", expand=False)
