"""
Test cases for the regi0.taxonomic.web.iucn.get_common_names function.
"""
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.iucn import get_common_names


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "name": "Loxodonta africana",
            "result": [
                {
                    "taxonname": "African Savanna Elephant",
                    "primary": True,
                    "language": "eng",
                },
                {"taxonname": "Savanna Elephant", "primary": False, "language": "eng"},
                {
                    "taxonname": "African Bush Elephant",
                    "primary": False,
                    "language": "eng",
                },
                {
                    "taxonname": "African Savannah Elephant",
                    "primary": False,
                    "language": "eng",
                },
                {"taxonname": "Savannah Elephant", "primary": False, "language": "eng"},
                {"taxonname": "Éléphant de savane", "primary": False, "language": "fre"},
                {"taxonname": "Elefante de Sabana", "primary": False, "language": "spa"},
            ],
        }


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


def test_success(success):
    result = get_common_names(
        "Loxodonta africana", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame(
        {
            "eng": [
                "African Savanna Elephant|Savanna Elephant|African Bush Elephant|African Savannah Elephant|Savannah Elephant"
            ],
            "fre": ["Éléphant de savane"],
            "spa": ["Elefante de Sabana"],
            "supplied_name": ["Loxodonta africana"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = get_common_names(
        "Ceroxylon sasaimae", token="221e3t9", add_supplied_names=True, expand=False
    )
    expected = pd.DataFrame({"supplied_name": ["Ceroxylon sasaimae"]})
    pd.testing.assert_frame_equal(result, expected)


def test_unauthorized(unauthorized):
    with pytest.raises(Exception):
        get_common_names("Loxodonta africana", token="551f4z6", expand=False)
