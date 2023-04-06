from qiskit import QuantumCircuit
from . import circuit_constructor, circuit_eq


def test_circuit_constructor():
    gates_list = ["h", "hs", "hs", "i", "i", "h"]
    result = circuit_constructor(gates_list)
    result_dag = circuit_constructor(gates_list, True)
    expected = QuantumCircuit(6)

    expected.h(0)
    _ = expected.s(1), expected.h(1)
    _ = expected.s(2), expected.h(2)
    expected.h(5)

    expected_dag = QuantumCircuit(6)

    expected_dag.h(0)
    _ = expected_dag.h(1), expected_dag.sdg(1)
    _ = expected_dag.h(2), expected_dag.sdg(2)
    expected_dag.h(5)

    assert circuit_eq(result, expected)
    assert circuit_eq(result_dag, expected_dag)
