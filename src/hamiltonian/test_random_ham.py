import pytest
from .random_hamiltonian import random_hamiltonian


# Have number of qubits large enough to have size number of unique Pauli ops.
qubits_list = [4, 8]
size_list = [1, 10]

paulis = ["i", "x", "y", "z"]


@pytest.mark.parametrize("size", size_list)
@pytest.mark.parametrize("qubit", qubits_list)
def test_gate_count_simple(size, qubit):
    ham = random_hamiltonian(qubit, size, 42)
    assert len(ham) == size

    for p, c in ham.items():
        assert len(p) == qubit
        for char in p:
            assert char in paulis
        assert -1 <= c <= 1
