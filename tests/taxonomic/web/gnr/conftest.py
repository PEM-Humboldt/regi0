"""
Configuration file for the regi0.taxonomic.web.gnr module tests.
"""
import pytest
import requests

success_json = {
    "id": "zves42fc59vn",
    "url": "http://resolver.globalnames.org/name_resolvers/zves42fc59vn.json",
    "data_sources": [{"id": 1, "title": "Catalogue of Life Checklist"}],
    "data": [
        {
            "supplied_name_string": "Panthera onca",
            "is_known_name": True,
            "results": [
                {
                    "data_source_id": 1,
                    "data_source_title": "Catalogue of Life Checklist",
                    "gni_uuid": "635db626-3f58-5caa-8148-4d77cd81d98d",
                    "name_string": "Panthera onca (Linnaeus, 1758)",
                    "canonical_form": "Panthera onca",
                    "classification_path": "Biota|Animalia|Chordata|Mammalia|Theria|Eutheria|Carnivora|Feliformia|Felidae|Pantherinae|Panthera|Panthera onca",
                    "classification_path_ranks": "unranked|kingdom|phylum|class|subclass|infraclass|order|suborder|family|subfamily|genus|species",
                    "classification_path_ids": "5T6MX|N|CH2|6224G|6226C|LG|VS|4DL|623RM|628LP|6DBT|4CGXQ",
                    "taxon_id": "4CGXQ",
                    "edit_distance": 0,
                    "imported_at": "2021-11-20T18:36:08Z",
                    "match_type": 2,
                    "match_value": "Exact match by canonical form",
                    "prescore": "3|0|0",
                    "score": 0.988,
                }
            ],
        },
        {
            "supplied_name_string": "Tremarctos ornatus",
            "is_known_name": True,
            "results": [
                {
                    "data_source_id": 1,
                    "data_source_title": "Catalogue of Life Checklist",
                    "gni_uuid": "c6b3c50b-f013-5125-aed0-81cc6d58b635",
                    "name_string": "Tremarctos ornatus (F. G. Cuvier, 1825)",
                    "canonical_form": "Tremarctos ornatus",
                    "classification_path": "Biota|Animalia|Chordata|Mammalia|Theria|Eutheria|Carnivora|Caniformia|Ursidae|Tremarctos|Tremarctos ornatus",
                    "classification_path_ranks": "unranked|kingdom|phylum|class|subclass|infraclass|order|suborder|family|genus|species",
                    "classification_path_ids": "5T6MX|N|CH2|6224G|6226C|LG|VS|4CT|HQQ|7YPQ|5832V",
                    "taxon_id": "5832V",
                    "edit_distance": 0,
                    "imported_at": "2021-11-20T19:03:46Z",
                    "match_type": 2,
                    "match_value": "Exact match by canonical form",
                    "prescore": "3|0|0",
                    "score": 0.988,
                }
            ],
        },
    ],
    "status": "success",
    "message": "Success",
    "parameters": {
        "with_context": False,
        "header_only": False,
        "with_canonical_ranks": False,
        "with_vernaculars": False,
        "best_match_only": False,
        "data_sources": [1],
        "preferred_data_sources": [],
        "resolve_once": False,
    },
}


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return success_json


class BadRequest(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 503


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: SuccessResponse())


@pytest.fixture()
def bad_request(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: BadRequest())
