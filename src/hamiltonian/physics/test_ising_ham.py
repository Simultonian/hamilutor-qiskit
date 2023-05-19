import pytest
from .ising import ising_1d


# Have number of qubits large enough to have size number of unique Pauli ops.
def test_ising_no_neigh():
    ham = ising_1d(1, 1.0, 1.0)
    expected = {"x": 1.0}
    assert ham == expected


def test_ising_one_neigh():
    ham = ising_1d(2, energy_prefactor=1.0, external_field=2.0, normalize=True)
    expected = {"xi": 2.0, "ix": 2.0, "zz": 1.0}
    expected = {p: v / sum(expected.values()) for p, v in expected.items()}

    assert ham == expected


def test_ising_two_neigh():
    ham = ising_1d(3, energy_prefactor=1.0, external_field=2.0, normalize=True)
    expected = {
        "xii": 2.0,
        "ixi": 2.0,
        "iix": 2.0,
        "zzi": 1.0,
        "izz": 1.0,
    }
    expected = {p: v / sum(expected.values()) for p, v in expected.items()}

    assert ham == expected
