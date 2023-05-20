import pytest
from .convert import to_pauli_op
from qiskit.quantum_info import SparsePauliOp


def test_convert_simple():
    ham = {"xxx": 1.0}
    exp = SparsePauliOp(["XXX"], [1.0])
    res = to_pauli_op(ham)
    assert exp == res


def test_convert_complex():
    ham = {"xxx": 1.0, "xyz": -1.0, "iii": 1.0}
    exp = SparsePauliOp(["XXX", "XYZ", "III"], [1.0, -1.0, 1.0])
    res = to_pauli_op(ham)
    assert exp == res
