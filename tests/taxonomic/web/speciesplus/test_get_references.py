"""
Test cases for the regi0.taxonomic.web.speciesplus.get_references function.
"""
import pandas as pd
import pytest
import requests

from regi0.taxonomic.web.speciesplus import get_references


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return [
            {
                "id": 7350,
                "citation": "Mills, J. 1992. Milking the bear trade. International Wildlife: 22: 38-45.",
                "is_standard": False,
            },
            {
                "id": 8103,
                "citation": "Thornback, L. J. and Jenkins, M. 1982. The IUCN mammal red data book, part 1. IUCN. Gland.",
                "is_standard": False,
            },
            {
                "id": 8255,
                "citation": "Weinhardt, D. 1994. International studbook for the Spectacled Bear <i>Tremarctos ornatus</i> 1992. ",
                "is_standard": False,
            },
            {
                "id": 43224,
                "citation": "Wilson, D.E. and Reeder, D.M. (Eds.). 2005. <i>Mammal species of the world, a taxonomic and geographic reference</i>. 3rd Edition, The Johns Hopkins University Press, Baltimore, Maryland. 2, 142pp.",
                "is_standard": True,
            },
            {
                "id": 18433,
                "citation": "Wilson, D.E. and Reeder, D.M. (Eds.). 2005. <i>Mammal species of the world, a taxonomic and geographic reference</i>. 3rd Edition, The Johns Hopkins University Press, Baltimore, Maryland. 2, 142pp.",
                "is_standard": False,
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
    result = get_references(
        "10071",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_ids=True,
        expand=False,
    )
    expected = pd.DataFrame(
        {
            "id": ["7350|8103|8255|43224|18433"],
            "citation": [
                "Mills, J. 1992. Milking the bear trade. International Wildlife: 22: "
                "38-45.|Thornback, L. J. and Jenkins, M. 1982. The IUCN mammal red data "
                "book, part 1. IUCN. Gland.|Weinhardt, D. 1994. International studbook "
                "for the Spectacled Bear <i>Tremarctos ornatus</i> 1992. |Wilson, D.E. "
                "and Reeder, D.M. (Eds.). 2005. <i>Mammal species of the world, a "
                "taxonomic and geographic reference</i>. 3rd Edition, The Johns Hopkins "
                "University Press, Baltimore, Maryland. 2, 142pp.|Wilson, D.E. and "
                "Reeder, D.M. (Eds.). 2005. <i>Mammal species of the world, a taxonomic "
                "and geographic reference</i>. 3rd Edition, The Johns Hopkins University"
                " Press, Baltimore, Maryland. 2, 142pp."
            ],
            "is_standard": ["False|False|False|True|False"],
            "supplied_id": ["10071"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = get_references(
        "2142412",
        token="bsgkp2kagTzJdQuywXnefAbc",
        add_supplied_ids=True,
        expand=False,
    )
    expected = pd.DataFrame({"supplied_id": ["2142412"]})
    pd.testing.assert_frame_equal(result, expected)


def test_unauthorized(unauthorized):
    with pytest.raises(requests.HTTPError):
        get_references(
            "10071",
            token="csgkp2kagTzJdQuywXnefAbz",
            add_supplied_ids=True,
            expand=False,
        )
