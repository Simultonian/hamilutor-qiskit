from qiskit import QuantumCircuit
from qiskit.opflow import X, Y, Z, I
from ..utils import qiskit_string_repr, circuit_eq
from .simple import trotter

import pytest

repr_hams = [
    {"xiizi": 1.0, "iyiiy": 2.0},
    {"iiizi": 1.0, "iyiiy": 2.0},
]

q_objs = [
    (1.0 * X ^ I ^ I ^ Z ^ I) + (2.0 * I ^ Y ^ I ^ I ^ Y),
    ((1.0) * I ^ I ^ I ^ Z ^ I) + ((2.0) * I ^ Y ^ I ^ I ^ Y),
]

gate_list = [["i", "i"], ["h", "i"], ["h", "hs"], ["i", "i"], ["i", "h"]]


@pytest.mark.parametrize("h,q_obj", zip(repr_hams, q_objs))
def test_qiskit_repr(h, q_obj):
    result = eval(qiskit_string_repr(h))
    assert result == q_obj


hamiltonians = [
    {"xiizi": 1.0},
    {"xiizi": 1.0, "iyiiy": 2.0},
]


@pytest.mark.parametrize("h", hamiltonians)
def test_trotter(h):
    result = trotter(h, 1.0)
    num_qubits = len(list(h.keys())[0])

    # It is equivalent of constructing individual term exponentiated and then
    # concatanating them.

    expected = QuantumCircuit(num_qubits)
    for pauli, coeff in h.items():
        cur = trotter({pauli: coeff})
        expected = expected.compose(cur)

    assert circuit_eq(expected, result)
