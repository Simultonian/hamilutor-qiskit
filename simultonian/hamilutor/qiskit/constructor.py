# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=too-many-instance-attributes
"""Base class for Hamiltonian Simulation functionality."""

from qiskit import QuantumCircuit  # type: ignore
from qiskit.circuit.library import PauliEvolutionGate  # type: ignore
from qiskit.opflow import PauliSumOp  # type: ignore
from .parser import Parser


class Constructor:
    """
        Base class for all the `qiskit` methods that can construct a circuit
        out of a Hamiltonian.
    """

    def __init__(self, method: str, optimizer=None, num_qubits=-1):
        self.method = method
        self.hamiltonian = ""
        self.circuit = None
        self.synthesizer = None
        self.circuit_optimizer = optimizer
        self.parser = Parser()
        self.pauli_op = None
        self.num_qubits = num_qubits

    def load_hamiltonian(self, hamiltonian: str, optimizer=None):
        """Load given Hamiltonian

        Loads the given Hamiltonian from the folder `hamiltonian/`.
        Hamiltonian when read from a file can further be optimized

        Args:
            - hamiltonian: name of the hamiltonian file
            - optimizer: callable that will take in the pauli_op and optimize
                         it.
        """
        self.hamiltonian = hamiltonian
        pauli_op: PauliSumOp = self.parser(hamiltonian)
        if optimizer is not None:
            pauli_op = optimizer(pauli_op)

        self.pauli_op = pauli_op

    def re_init(self):
        """
        Re-initialize the synthesizer for the construction of circuit.
        """
        raise NotImplementedError("Accessing superclass is not allowed")

    def get_circuit(self) -> QuantumCircuit:
        """Get Hamiltonian circuit.

        Get the higher level circuit for the Hamiltonian.
        Note that the circuit must be converted to fundamental gates for
        measuring the gate depth.

        Returns:
            Quantum Circuit for the loaded hamiltonian.
        """
        evo_gate = PauliEvolutionGate(
            self.pauli_op, 1.0, synthesis=self.synthesizer)

        if self.num_qubits == -1:
            num_qubits = evo_gate.num_qubits
            self.num_qubits = num_qubits
        # reset circuit everytime to avoid pile-up
        circ = QuantumCircuit(self.num_qubits)
        circ.append(evo_gate, list(range(self.num_qubits)))

        self.circuit = circ
        return circ
