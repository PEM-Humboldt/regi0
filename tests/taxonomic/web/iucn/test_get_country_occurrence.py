"""
Test cases for the regi0.taxonomic.web.iucn.get_country_occurrence function.
"""
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.iucn import get_country_occurrence


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "name": "Bradypus variegatus",
            "count": 11,
            "result": [
                {
                    "code": "AR",
                    "country": "Argentina",
                    "presence": "Possibly Extinct",
                    "origin": "Native",
                    "distribution_code": "Possibly Extinct",
                },
                {
                    "code": "BO",
                    "country": "Bolivia, Plurinational State of",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "BR",
                    "country": "Brazil",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "CO",
                    "country": "Colombia",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "CR",
                    "country": "Costa Rica",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "EC",
                    "country": "Ecuador",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "HN",
                    "country": "Honduras",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "NI",
                    "country": "Nicaragua",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "PA",
                    "country": "Panama",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "PE",
                    "country": "Peru",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
                {
                    "code": "VE",
                    "country": "Venezuela, Bolivarian Republic of",
                    "presence": "Extant",
                    "origin": "Native",
                    "distribution_code": "Native",
                },
            ],
        }


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


def test_success(success):
    result = get_country_occurrence(
        "Bradypus variegatus", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame(
        {
            "code": ["AR|BO|BR|CO|CR|EC|HN|NI|PA|PE|VE"],
            "country": [
                "Argentina|Bolivia, Plurinational State of|Brazil|Colombia|Costa Rica|Ecuador|Honduras|Nicaragua|Panama|Peru|Venezuela, Bolivarian Republic of",
            ],
            "presence": [
                "Possibly Extinct|Extant|Extant|Extant|Extant|Extant|Extant|Extant|Extant|Extant|Extant",
            ],
            "origin": [
                "Native|Native|Native|Native|Native|Native|Native|Native|Native|Native|Native",
            ],
            "distribution_code": [
                "Possibly Extinct|Native|Native|Native|Native|Native|Native|Native|Native|Native|Native",
            ],
            "supplied_name": ["Bradypus variegatus"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = get_country_occurrence(
        "Ceroxylon sasaimae", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame({"supplied_name": ["Ceroxylon sasaimae"]})
    pd.testing.assert_frame_equal(result, expected)

def test_unauthorized(unauthorized):
    with pytest.raises(Exception):
        get_country_occurrence("Bradypus variegatus", token="551f4z6", expand=False)
