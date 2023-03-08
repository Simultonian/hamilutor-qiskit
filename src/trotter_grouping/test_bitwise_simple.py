import pytest
from qiskit import QuantumCircuit
from ..trotter.simple import trotter, _circuit_eq
from .bitwise_simple import bitwise_simple

repr_hams = [
    {"xx": 1.0, "yy": 2.0, "zz": 3.0, "ii": -4.0, "iz": 5.0},
    {"xiizi": 1.0, "iyiiy": 2.0, "ziizi": 2.0},
    {"iiizz": 1.0, "iyiiy": 2.0},
]

groups_list = [
    [{"xx": 1.0, "ii": -4.0}, {"yy": 2.0}, {"zz": 3.0, "iz": 5.0}],
    [{"xiizi": 1.0, "iyiiy": 2.0}, {"ziizi": 2.0}],
    [{"iiizz": 1.0}, {"iyiiy": 2.0}],
]

num_qubits_list = [2, 5, 5]


@pytest.mark.parametrize(
    "h,groups,qubits", zip(repr_hams, groups_list, num_qubits_list)
)
def test_qiskit_repr(h, groups, qubits):
    result = bitwise_simple(h)

    expected = QuantumCircuit(qubits)

    for group in groups:
        for pauli, coeff in group.items():
            cur = trotter({pauli: coeff})
            expected = expected.compose(cur)

    assert _circuit_eq(result, expected)
