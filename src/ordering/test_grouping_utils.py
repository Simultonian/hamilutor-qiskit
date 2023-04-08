import pytest
from .lexico import lexico


pauli_lists = [["ziz", "iiz", "zzz"]]
ordered = [["iiz", "ziz", "zzz"]]


@pytest.mark.parametrize("pauli_list,ordered", zip(pauli_lists, ordered))
def test_op_order(pauli_list, ordered):
    result = lexico(pauli_list)
    for a, b in zip(result, ordered):
        assert a == b
