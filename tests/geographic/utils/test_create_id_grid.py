"""
Test cases for the bdcctools.geographic.utils.create_id_grid function.
"""
import numpy as np
import pytest

from bdcctools.geographic.utils import create_id_grid


@pytest.fixture(scope="module")
def matching_grid():
    return create_id_grid(-1.0, -1.0, 2.0, 4.0, 0.25)


@pytest.fixture(scope="module")
def unmatching_grid():
    return create_id_grid(1.0, 1.0, 4.0, 4.0, 0.33)


def test_width(matching_grid):
    assert matching_grid.width == 12


def test_height(matching_grid):
    assert matching_grid.height == 20


def test_origin(matching_grid):
    assert matching_grid.transform.c == -1.0 and matching_grid.transform.f == 4.0


def test_resolution(matching_grid):
    assert matching_grid.transform.a == 0.25 and matching_grid.transform.e == -0.25


def test_unique(matching_grid):
    arr = matching_grid.read(1)
    assert arr.size == np.unique(arr).size


def test_unmatching_bounds(unmatching_grid):
    bounds = unmatching_grid.bounds
    assert bounds.bottom < 1.0 and bounds.right > 4.0


def test_force_origin(unmatching_grid):
    assert unmatching_grid.transform.c == 1.0 and unmatching_grid.transform.f == 4.0


def test_other_crs():
    grid = create_id_grid(0, 0, 1000, 1000, 100, crs="epsg:3857")
    assert grid.crs.to_string() == "EPSG:3857"
