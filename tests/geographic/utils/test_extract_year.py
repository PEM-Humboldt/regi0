"""
Test cases for the bdcctools.geographic.utils.extract_year function.
"""
import pytest

from bdcctools.geographic.utils import extract_year


def test_separate():
    assert extract_year("admin2_2014.shp") == 2014


def test_joined():
    assert extract_year("v0001popc2017") == 2017


def test_multiple():
    assert extract_year("human_footprint_1970_1990.tif") == 1970


def test_no_four_digit_num():
    with pytest.raises(Exception):
        extract_year("ne_10m_admin_o_countries.shp")


def test_no_four_digit_year():
    with pytest.raises(Exception):
        extract_year("v0001popc")
