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
from qiskit.quantum_info import Operator
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller

from simultonian.hamilutor.qiskit import Lie
from simultonian.hamilutor.qiskit.circuit_optimizer import Dummy


def _decompose_circuit(
    circuit: QuantumCircuit, gate_set: Optional[List] = None
) -> Union[QuantumCircuit, List[QuantumCircuit]]:
    if gate_set is None:
        gate_set = ["cx", "u"]

    transpile_pass = Unroller(gate_set)
    manager = PassManager(transpile_pass)
    return manager.run(circuit)


@pytest.mark.parametrize(['h_str'], [("""1 Z""",)])
def test_dummy_same_constructor(h_str: str):
    """
    Validity of Circuit constructed for `H = P`
    """
    optimizer = Dummy()
    lie = Lie(circuit_optimizer=optimizer)
    lie.load_hamiltonian_string(h_str)

    circ = _decompose_circuit(lie.get_circuit())
    optimized_circ = _decompose_circuit(lie.get_circuit(optimize=True))
    assert Operator(circ).equiv(Operator(optimized_circ))


def test_dummy_non_circuit():
    optimizer = Dummy()

    with pytest.raises(ValueError, match="Incorrect type"):
        optimizer(None)

    with pytest.raises(ValueError, match="Incorrect type"):
        optimizer(1)
