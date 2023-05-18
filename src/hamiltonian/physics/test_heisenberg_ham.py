import pytest
from .heisenberg import heisenberg_xxz


def test_heisenberg_one_neigh():
    ham = heisenberg_xxz(2, coupling_field=1.0, external_field=2.0)
    expected = {"xx": 1.0, "yy": 1.0, "zz": 2.0}
    expected = {p: v / sum(expected.values()) for p, v in expected.items()}

    assert ham == expected


def test_heisenberg_two_neigh():
    ham = heisenberg_xxz(3, coupling_field=1.0, external_field=2.0)
    expected = {
        "xxi": 1.0,
        "yyi": 1.0,
        "zzi": 2.0,
        "ixx": 1.0,
        "iyy": 1.0,
        "izz": 2.0,
    }
    expected = {p: v / sum(expected.values()) for p, v in expected.items()}

    assert ham == expected
