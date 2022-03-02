"""
Test cases for the regi0.taxonomic.web.gnr.resolve function.
"""
import pandas as pd
import pytest

from regi0.taxonomic.web.gnr import resolve


def test_success(success):
    result = resolve(
        ["Panthera onca", "Tremarctos ornatus"], data_source_ids=["1"], expand=False
    )
    expected = pd.DataFrame(
        {
            "data_source_id": [1, 1],
            "data_source_title": [
                "Catalogue of Life Checklist",
                "Catalogue of Life Checklist",
            ],
            "gni_uuid": [
                "635db626-3f58-5caa-8148-4d77cd81d98d",
                "c6b3c50b-f013-5125-aed0-81cc6d58b635",
            ],
            "name_string": [
                "Panthera onca (Linnaeus, 1758)",
                "Tremarctos ornatus (F. G. Cuvier, 1825)",
            ],
            "canonical_form": ["Panthera onca", "Tremarctos ornatus"],
            "classification_path": [
                "Biota|Animalia|Chordata|Mammalia|Theria|Eutheria|Carnivora|Feliformia|Felidae|Pantherinae|Panthera|Panthera onca",
                "Biota|Animalia|Chordata|Mammalia|Theria|Eutheria|Carnivora|Caniformia|Ursidae|Tremarctos|Tremarctos ornatus",
            ],
            "classification_path_ranks": [
                "unranked|kingdom|phylum|class|subclass|infraclass|order|suborder|family|subfamily|genus|species",
                "unranked|kingdom|phylum|class|subclass|infraclass|order|suborder|family|genus|species",
            ],
            "classification_path_ids": [
                "5T6MX|N|CH2|6224G|6226C|LG|VS|4DL|623RM|628LP|6DBT|4CGXQ",
                "5T6MX|N|CH2|6224G|6226C|LG|VS|4CT|HQQ|7YPQ|5832V",
            ],
            "taxon_id": ["4CGXQ", "5832V"],
            "edit_distance": [0, 0],
            "imported_at": ["2021-11-20T18:36:08Z", "2021-11-20T19:03:46Z"],
            "match_type": [2, 2],
            "match_value": [
                "Exact match by canonical form",
                "Exact match by canonical form",
            ],
            "prescore": ["3|0|0", "3|0|0"],
            "score": [0.988, 0.988],
            "supplied_name_string": ["Panthera onca", "Tremarctos ornatus"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_no_result(no_result):
    result = resolve("Ceroxylon sasaimae", data_source_ids=["5"], expand=False)
    expected = pd.DataFrame({"supplied_name_string": ["Ceroxylon sasaimae"]})
    pd.testing.assert_frame_equal(result, expected)


def test_bad_request(bad_request):
    with pytest.raises(Exception):
        resolve(
            ["Panthera onca", "Tremarctos ornatus"], data_source_ids=["1"], expand=False
        )
