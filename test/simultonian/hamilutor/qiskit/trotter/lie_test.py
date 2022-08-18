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

from typing import Optional, List, Union
import pytest
from qiskit import QuantumCircuit  # type: ignore
from qiskit.transpiler.passes import Unroller
from qiskit.transpiler import PassManager
from qiskit.quantum_info import Operator

from simultonian.hamilutor.qiskit import Lie


def _decompose_circuit(
    circuit: QuantumCircuit, gate_set: Optional[List] = None
) -> Union[QuantumCircuit, List[QuantumCircuit]]:
    if gate_set is None:
        gate_set = ["cx", "u"]

    transpile_pass = Unroller(gate_set)
    manager = PassManager(transpile_pass)
    return manager.run(circuit)


def _construct_circuit(qubits: int, gates) -> QuantumCircuit:
    circuit = QuantumCircuit(qubits)
    for gate_name, params in gates:
        getattr(circuit, gate_name)(*params)

    return circuit


@pytest.mark.parametrize(['h_str', 'gates', 'qubits'], [
    ("""1 Z""", [('u', (0, 0, 2, 0))], 1),
])
def test_lie(h_str: str, gates, qubits: int):
    """
    Validity of Circuit constructed for `H = P`
    """
    lie = Lie()
    lie.load_hamiltonian_string(h_str)
    circ = _decompose_circuit(lie.get_circuit())
    expected_circ = _construct_circuit(qubits, gates)
    assert Operator(circ).equiv(Operator(expected_circ))
