from qiskit.opflow import X, Y, Z, I
from .simple import _qiskit_string_repr, _circuit_eq, trotter

import pytest

repr_hams = [
        [(1.0, "xiizi"), (2.0, "iyiiy")],
        [(1.0, "iiizi"), (2.0, "iyiiy")],
        ]

q_objs = [
        (1.0 * X^I^I^Z^I) + (2.0 * I^Y^I^I^Y),
        ((1.0) * I^I^I^Z^I) + ((2.0) * I^Y^I^I^Y),
        ]

gate_list = [["i", "i"], ["h", "i"], ["h", "hs"], ["i", "i"], ["i", "h"]]

@pytest.mark.parametrize("h,q_obj", zip(repr_hams, q_objs))
def test_qiskit_repr(h, q_obj):
    result = eval(_qiskit_string_repr(h))
    assert result == q_obj


hamiltonians = [
        [(1.0, "xiizi")],
        [(1.0, "xiizi"), (2.0, "iyiiy")],
        [(1.0, "iiizi"), (2.0, "iyiiy")],
        ]

@pytest.mark.parametrize("h", hamiltonians)
def test_trotter(h):
    result = trotter(h, 1.0)

    # It is equivalent of constructing individual term exponentiated and then
    # concatanating them.

    expected = None
    for term in h:
        cur = trotter([term])
        if expected is None:
            expected = cur
        else:
            expected = expected.compose(cur)
    
    assert _circuit_eq(expected, result)
