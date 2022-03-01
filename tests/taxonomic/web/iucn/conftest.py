"""
Configuration file for the regi0.taxonomic.web.iucn module tests.
"""
import pytest
import requests


class NoResult(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {"name": "Ceroxylon sasaimae", "result": []}


class Unauthorized(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self, **kwargs):
        return {"message": "Token not valid!"}


@pytest.fixture()
def no_result(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: NoResult())


@pytest.fixture()
def unauthorized(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Unauthorized())
