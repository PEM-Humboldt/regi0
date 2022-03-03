"""
Configuration file for the regi0.taxonomic.web.speciesplus module tests.
"""
import pytest
import requests


class Unauthorized(requests.Response):
    def __init__(self):
        super().__init__()
        self.status_code = 401

@pytest.fixture()
def unauthorized(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Unauthorized())
