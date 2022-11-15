# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Lie Trotter testing."""

from typing import List, Optional, Union

import pytest
from qiskit import QuantumCircuit  # type: ignore
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller

from simultonian.hamilutor.qiskit import Lie, Parser
from simultonian.hamilutor.qiskit.sampler import Identity as SamplerIdentity
from simultonian.hamilutor.qiskit.circuit_optimizer import (
    Identity as CircuitIdentity)


def _decompose_circuit(
    circuit: QuantumCircuit, gate_set: Optional[List] = None
) -> Union[QuantumCircuit, List[QuantumCircuit]]:
    if gate_set is None:
        gate_set = ["cx", "u"]

    transpile_pass = Unroller(gate_set)
    manager = PassManager(transpile_pass)
    return manager.run(circuit)


@pytest.mark.parametrize(['h_str'], [("""1 Z""",)])
def test_identity_same_constructor(h_str: str):
    """
    Validity of Circuit constructed for `H = P`
    """
    parser = Parser()
    parser.load(h_str)

    hamiltonian = SamplerIdentity()
    hamiltonian.load(parser.roll())

    lie = Lie(num_qubits=1)
    lie.load(hamiltonian)
    circ = lie.roll()

    optimizer = CircuitIdentity()
    optimized_circ = optimizer(circ)

    for x, y in zip(circ, optimized_circ):
        assert x == y


def test_identity_non_circuit():
    optimizer = CircuitIdentity()

    with pytest.raises(ValueError, match="Incorrect type"):
        optimizer(None)

    with pytest.raises(ValueError, match="Incorrect type"):
        optimizer(1)
