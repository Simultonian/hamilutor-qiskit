from qiskit import QuantumCircuit
from ..utils import circuit_eq
from .simple import qdrift
from ..trotter.simple import trotter

import numpy as np
import pytest

hamiltonians = [
    {"xx": 1.0, "iy": 1.0},
    {"xi": 1.0},
]

order_list = [
        ["iy", "iy", "iy", "iy", "xx", "iy", "xx", "iy"],
        ["xi", "xi"], 
        ]



@pytest.mark.parametrize("h,order", zip(hamiltonians,order_list))
def test_qdrift(h,order):
    # Setting random seed for testing
    np.random.seed(0)

    result = qdrift(h, 1.0)
    num_qubits = len(list(h.keys())[0])

    lambd = sum(list(h.values()))
    N = 2 * (lambd**2)
    factor = lambd / N

    # It is equivalent of constructing individual term exponentiated and then
    # concatanating them.

    expected = QuantumCircuit(num_qubits)
    for term in order:
        cur = trotter({term: factor / h[term]})
        expected = expected.compose(cur)

    assert circuit_eq(expected, result)
