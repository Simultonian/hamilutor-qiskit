import pytest
from qiskit import QuantumCircuit
from ..trotter.simple import trotter
from ..utils import circuit_eq
from .group_trotter import generic

from ..grouping import Bitwise
from ..ordering import lexico

import itertools


def test_single_group_trotter_grouper():
    group = {"ix": 1.0, "xi": -1.0}

    result = generic(Bitwise, lexico, group)

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
        result = generic(Bitwise, lexico, group, t=1.0, reps=reps)

        expected = QuantumCircuit(2)

        for _ in range(reps):
            # Rotation
            expected.h(0)
            expected.h(1)

            # Exponentiate
            circuit = trotter({"iz": 1.0, "zi": -1.0}, t=1.0 / reps)
            expected = expected.compose(circuit)

            # Anti-rotation
            expected.h(0)
            expected.h(1)

        assert circuit_eq(result, expected)


two_group_hams = [
    {"xx": 1.0, "zz": 2.0},
    {"xx": 1.0, "zz": 2.0, "zi": 3.0},
    {"xx": 1.0, "zz": 2.0, "zi": 3.0, "xy": 4.0},
]
two_group_groups = [
    [
        {"xx": 1.0},
        {"zz": 2.0},
    ],
    [
        {"xx": 1.0},
        {"zz": 2.0, "zi": 3.0},
    ],
    [{"xx": 1.0}, {"zz": 2.0, "zi": 3.0}, {"xy": 4.0}],
]
two_num_qubits = [2, 2]


@pytest.mark.parametrize("reps", range(1, 5))
@pytest.mark.parametrize(
    "h,groups,qubits", zip(two_group_hams, two_group_groups, two_num_qubits)
)
def test_bitwise_simple_multiple_groups(reps, h, groups, qubits):
    # Checking for multiple number of repetitions.
    result = generic(Bitwise, lexico, h, t=1.0, reps=reps)

    check = False

    # Check for all possible orders of the group
    for order in itertools.permutations(groups):
        expected = QuantumCircuit(qubits)
        # Runs reps loop and trotters individual group.
        for _ in range(reps):
            for group in order:
                circuit = trotter(group, t=1.0 / reps)
                expected = expected.compose(circuit)

        check = check or circuit_eq(result, expected)

    assert check
