"""
Configuration file for the regi0.geographic.web.arcgis module tests.
"""
import pytest
import requests


class SuccessResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "id": "0",
                    "type": "Feature",
                    "properties": {"dptos": "SANTANDER", "fid": 4.0},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-73.21752935323963, 6.562170940611484],
                                [-74.57644315124725, 6.2039350030896525],
                                [-73.77704340199992, 8.142174027000065],
                                [-71.95538682324725, 6.996811748089653],
                                [-73.21752935323963, 6.562170940611484],
                            ]
                        ],
                    },
                },
                {
                    "id": "1",
                    "type": "Feature",
                    "properties": {"dptos": "BOYACA", "fid": 22.0},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-73.03057881399992, 4.982293329000066],
                                [-74.65938395399992, 5.748359847000065],
                                [-74.57644315124725, 6.2039350030896525],
                                [-73.21752935323963, 6.562170940611484],
                                [-71.95538682324725, 6.996811748089653],
                                [-73.03057881399992, 4.982293329000066],
                            ]
                        ],
                    },
                },
            ],
        }


class ErrorResponse(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {
            "error": {
                "code": 400,
                "message": "Cannot perform query. Invalid query parameters.",
                "details": ["Unable to perform query. Please check your parameters."],
            }
        }


class BadRequest(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 400


@pytest.fixture()
def success(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: SuccessResponse())


@pytest.fixture()
def error(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: ErrorResponse())


@pytest.fixture()
def bad_request(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: BadRequest())
