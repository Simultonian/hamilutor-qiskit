import pytest
from qiskit import QuantumCircuit
from ..trotter.simple import trotter
from ..utils import circuit_eq
from .bitwise_simple import bitwise_simple, _circuit_constructor, group_trotter

def test_circuit_constructor():
    gates_list = ["h", "hs", "hs", "i", "i", "h"]
    result = _circuit_constructor(gates_list)
    result_dag = _circuit_constructor(gates_list, True)
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


def test_single_group_trotter():
    group = {"ix": 1.0, "xi": -1.0}

    result = group_trotter(group)

    expected = QuantumCircuit(2)

    # Rotation
    expected.h(0)
    expected.h(1)

    # Exponentiate
    circuit = trotter({"iz": 1.0, "zi": -1.0})
    expected = expected.compose(circuit)

    # Anti-rotation
    expected.h(0)
    expected.h(1)

    assert circuit_eq(result, expected)


def test_bitwise_simple_single_group():
    group = {"ix": 1.0, "xi": -1.0}

    # Checking for multiple number of repetitions
    for reps in range(1, 5):
        result = bitwise_simple(group, t=1.0, reps=reps)

        expected = QuantumCircuit(2)

        for _ in range(reps):
            # Rotation
            expected.h(0)
            expected.h(1)

            # Exponentiate
            circuit = trotter({"iz": 1.0, "zi": -1.0}, t=1.0/reps)
            expected = expected.compose(circuit)

            # Anti-rotation
            expected.h(0)
            expected.h(1)

        assert circuit_eq(result, expected)



two_group_hams = [
        {"xx": 1.0, "zz": 2.0},
        {"xx": 1.0, "zz": 2.0, "zi":3.0},
        {"xx": 1.0, "zz": 2.0, "zi":3.0, "xy": 4.0},
        ]
two_group_groups = [
        [{"xx": 1.0}, {"zz": 2.0},],
        [{"xx": 1.0}, {"zz": 2.0, "zi":3.0},],
        [{"xx": 1.0}, {"zz": 2.0, "zi":3.0}, {"xy":4.0}],
        ]
two_num_qubits = [2, 2]

@pytest.mark.parametrize("h,groups,qubits", zip(two_group_hams, two_group_groups, two_num_qubits))
def test_bitwise_simple_multiple_groups(h,groups,qubits):

    # Checking for multiple number of repetitions.
    for reps in range(1, 5):
        result = bitwise_simple(h, t=1.0, reps=reps)

        expected = QuantumCircuit(qubits)

        # Runs reps loop and trotters individual group.
        for _ in range(reps):
            for group in groups:
                circuit = group_trotter(group, t=1.0/reps)
                expected = expected.compose(circuit)


        assert circuit_eq(result, expected)
