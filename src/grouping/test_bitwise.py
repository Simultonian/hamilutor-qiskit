import pytest
from .bitwise import (
    bitwise_group,
    bitwise_representor,
    bitwise_gate,
    bitwise_operator_convertor,
)

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
def test_commuting(pauli_list, grouped):
    result = bitwise_group(pauli_list)
    assert sorted(result) == sorted(grouped)


comm_pauli_sets = [["zz", "ii"], ["xz", "xi", "ii"], ["ix", "xi"], ["ii"], ["ix", "ii"]]

representations = ["zz", "xz", "xx", "ii", "ix"]


@pytest.mark.parametrize("pauli_list,reprs", zip(comm_pauli_sets, representations))
def test_representations(pauli_list, reprs):
    result = bitwise_representor(pauli_list)
    assert result == reprs


representations = ["zz", "xz", "xy", "ii", "ix"]
gate_list = [["i", "i"], ["h", "i"], ["h", "hs"], ["i", "i"], ["i", "h"]]


@pytest.mark.parametrize("reprs,gates", zip(representations, gate_list))
def test_bitwise_gate(reprs, gates):
    result = bitwise_gate(reprs)
    assert sorted(result) == sorted(gates)


paulis = ["zz", "xz", "xy", "ii", "ix"]
diags = [(1.0, "zz"), (1.0, "zz"), (-1.0, "zz"), (1.0, "ii"), (1.0, "iz")]


@pytest.mark.parametrize("pauli,diag", zip(paulis, diags))
def test_bitwise_conversion(pauli, diag):
    result = bitwise_operator_convertor(pauli)
    assert result == diag
