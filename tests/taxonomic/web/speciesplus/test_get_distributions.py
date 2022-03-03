"""
Test cases for the regi0.taxonomic.web.speciesplus.get_distributions function.
"""
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.speciesplus import get_distributions


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return [
            {
                "id": 15783,
                "iso_code2": "BO",
                "name": "Bolivia (Plurinational State of)",
                "tags": [],
                "type": "COUNTRY",
                "references": [
                    "Cabrera, A. 1957.",
                    "Ergueta S., P. and de Morales, C (eds.) 1996.",
                    "Wilson, D.E. and Reeder, D.M. (Eds.). 2005.",
                ],
            },
            {
                "id": 19707,
                "iso_code2": "PE",
                "name": "Peru",
                "tags": [],
                "type": "COUNTRY",
                "references": [
                    "Cabrera, A. 1957.",
                    "Eisenberg, J. F. 1989.",
                    "Grimwood, I. R. 1969.",
                    "Pacheco, V., de Macedo, H., Vivar, E. 1995.",
                    "Pacheco, V., Patterson, B. D., Patton, J. L., Emmons, L. H. 1993.",
                    "Wilson, D.E. and Reeder, D.M. (Eds.). 2005.",
                ],
            },
            {
                "id": 25560,
                "iso_code2": "PA",
                "name": "Panama",
                "tags": ["distribution uncertain"],
                "type": "COUNTRY",
                "references": ["Wilson, D.E. and Reeder, D.M. (Eds.). 2005."],
            },
            {
                "id": 33202,
                "iso_code2": "CO",
                "name": "Colombia",
                "tags": [],
                "type": "COUNTRY",
                "references": [
                    "Alberico, M., Cadena, A., Hernández-Camacho, J. and Muñoz-Saba, Y. 2000.",
                    "Cabrera, A. 1957.",
                    "Eisenberg, J. F. 1989.",
                    "Kattan, G., Heranández, O. L., Goldstein, I., 2004.",
                    "Wilson, D.E. and Reeder, D.M. (Eds.). 2005.",
                ],
            },
            {
                "id": 38337,
                "iso_code2": "EC",
                "name": "Ecuador",
                "tags": [],
                "type": "COUNTRY",
                "references": [
                    "Kattan, G., Heranández, O. L., Goldstein, I., Rojas, V., Murillo, O. 2004.",
                    "Wilson, D.E. and Reeder, D.M. (Eds.). 2005.",
                ],
            },
            {
                "id": 62316,
                "iso_code2": "VE",
                "name": "Venezuela (Bolivarian Republic of)",
                "tags": [],
                "type": "COUNTRY",
                "references": [
                    "Bisbal, F. J. 1993.",
                    "Kattan, G., Heranández, O. L., Goldstein, I., Rojas, V., Murillo, O., Gómez, C., Restrepo, H. and Cuesta, F. 2004. ",
                    "Rodríguez, J. P. and Rojas-Suárez, F. 1999.",
                    "Wilson, D.E. and Reeder, D.M. (Eds.). 2005.",
                ],
            },
            {
                "id": 76073,
                "iso_code2": "AR",
                "name": "Argentina",
                "tags": ["distribution uncertain"],
                "type": "COUNTRY",
                "references": ["Wilson, D.E. and Mittermeier, R.A. 2009."],
            },
        ]


class NoResult(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 500


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: SuccessResponse())


@pytest.fixture()
def no_result(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: NoResult())


def test_success(success):
    result = get_distributions(
        "10071",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_ids=True,
        expand=False,
    )
    expected = pd.DataFrame(
        {
            "id": ["15783|19707|25560|33202|38337|62316|76073"],
            "iso_code2": ["BO|PE|PA|CO|EC|VE|AR"],
            "name": [
                "Bolivia (Plurinational State of)|Peru|Panama|Colombia|Ecuador|Venezuela (Bolivarian Republic of)|Argentina"
            ],
            "type": ["COUNTRY|COUNTRY|COUNTRY|COUNTRY|COUNTRY|COUNTRY|COUNTRY"],
            "supplied_id": "10071"
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = get_distributions(
        "2142412",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_ids=True,
        expand=False,
    )
    expected = pd.DataFrame({"supplied_id": ["2142412"]})
    pd.testing.assert_frame_equal(result, expected)


def test_unauthorized(unauthorized):
    with pytest.raises(requests.HTTPError):
        get_distributions(
            "10071",
            token="csgkp2kagTzJdQuywXnefAbz",
            add_supplied_ids=True,
            expand=False,
        )
