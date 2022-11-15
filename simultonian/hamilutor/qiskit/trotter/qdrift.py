# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""QDRIFT functionality for constructing circuits."""

from qiskit import QuantumCircuit
from ..circuit_maker import CircuitMaker
from ..sampler import Identity
from ..parser import PauliSequence

from qiskit.synthesis import QDrift
from qiskit.opflow import PauliSumOp
from qiskit.circuit.library import PauliEvolutionGate


class Lie(CircuitMaker):
    """Lie Trotter method

       Using the standard method that is in-built in qiskit.
    """

    def __init__(self, num_qubits: int = -1):
        super().__init__("LIE", num_qubits)

    def load(self, sampler: Identity, **kwargs) -> None:
        """Load the Sampler

        Args:
            - sampler: Sampler that will let the circuit maker get
            PauliSequences.
        """
        reps = kwargs.get('reps', 1)
        time = kwargs.get('t', 1.0)

        pauli_list: PauliSequence = [pauli for pauli_seq in sampler.sample()
                                     for pauli in pauli_seq]
        pauli_op = PauliSumOp.from_list(pauli_list)

        # TODO Look into `atomic_evolution` argument that can be used
        synthesizer = QDrift(reps=reps)
        evo_gate = PauliEvolutionGate(pauli_op, time, synthesis=synthesizer)
        if self.num_qubits == -1:
            self.num_qubits = int(evo_gate.num_qubits)

        circ = QuantumCircuit(self.num_qubits)
        circ.append(evo_gate, list(range(self.num_qubits)))

        self.circuit = circ

    def roll(self) -> QuantumCircuit:
        return self.circuit
