import pytest
from .bitwise import bitwise_group

pauli_lists = [
        ["zz", "xi", "ii", "yy"],
        ["zz", "xi", "ii"],
        ["ix", "xi", "ii"],
        ["ix", "xi"],
        [],
]

groupeds = [
        [["zz", "ii"], ["xi"], ["yy"]],
        [["zz", "ii"], ["xi"]],
        [["ix", "xi", "ii"]],
        [["ix", "xi"]],
        [],
]

@pytest.mark.parametrize("pauli_list,grouped", zip(pauli_lists, groupeds))
def test_commuting(pauli_list,grouped):
    result = bitwise_group(pauli_list)
    assert sorted(result) == sorted(grouped)
