# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=too-many-instance-attributes, fixme
"""Base class for Hamiltonian Simulation functionality."""

from typing import Optional

from qiskit import QuantumCircuit  # type: ignore
from qiskit.circuit.library import PauliEvolutionGate  # type: ignore

from .circuit_optimizer import CircuitOptimizer
from .operator import Hamiltonian
from .parser import Parser


class Constructor:
    """
        Base class for all the `qiskit` methods that can construct a circuit
        out of a Hamiltonian.
    """

    def __init__(
            self,
            method: str,
            circuit_optimizer: Optional[CircuitOptimizer] = None,
            hamiltonian_optimizer=None,
            num_qubits=-1):
        """
            Base class for all the `qiskit` methods that can construct a
            circuit out of a Hamiltonian.

            Args:
                - method: Method Name used for constructing the circuit
                - circuit_optimizer:
        """
        self.method = method
        self.num_qubits = num_qubits
        self.circuit_optimizer = circuit_optimizer
        # TODO: Create a base class for Hamiltonian optimizer
        self.hamiltonian_optimizer = hamiltonian_optimizer

        self.parser = Parser()

        self.hamiltonian = ""
        self.circuit = None
        self.synthesizer = None
        self.pauli_op: Optional[Hamiltonian] = None

    def load_hamiltonian(self, hamiltonian: str, optimizer=None):
        """Load given Hamiltonian

        Loads the given Hamiltonian. Hamiltonian when read from a file can
        further be optimized.

        # TODO: Create a base class for Hamiltonian optimizer
        Args:
            - hamiltonian: path of the file.
            - optimizer: callable that will take in the pauli_op and optimize
                         it.
        """
        self.hamiltonian = hamiltonian
        self.pauli_op = self.parser(hamiltonian)

        if optimizer is not None:
            optimizer(self.pauli_op)

    def load_hamiltonian_string(self, h_string: str, optimizer=None):
        """Load given Hamiltonian

        Loads the given Hamiltonian from the folder `hamiltonian/`.
        Hamiltonian when read from a file can further be optimized

        Args:
            - hamiltonian: hamiltonian string
            - optimizer: callable that will take in the pauli_op and optimize
                         it.
        """
        self.pauli_op = self.parser.parse_pauli(h_string)
        if optimizer is not None:
            optimizer(self.pauli_op)

        elif self.hamiltonian_optimizer is not None:
            self.hamiltonian_optimizer(self.pauli_op)

    def optimize_hamiltonian(self, optimizer=None):
        """
        Run the given optimizer on the Hamiltonian. If no optimizer is not
        passed then the method will use self.hamiltonian_optimizer.
        """
        if optimizer is None:
            if self.hamiltonian_optimizer is None:
                raise ValueError("Hamiltonian Optimizer was not passed.")
            self.hamiltonian_optimizer(self.pauli_op)
        else:
            optimizer(self.pauli_op)

    def re_init(self):
        """
        Re-initialize the synthesizer for the construction of circuit.
        """
        raise NotImplementedError("Accessing superclass is not allowed")

    def get_circuit(self, optimize=False) -> QuantumCircuit:
        """Get Hamiltonian circuit.

        Get the higher level circuit for the Hamiltonian.
        Note that the circuit must be converted to fundamental gates for
        measuring the gate depth.

        Returns:
            Quantum Circuit for the loaded hamiltonian.
        """
        if self.pauli_op is None:
            raise AttributeError("Pauli operator has not been set")
        evo_gate = PauliEvolutionGate(
            self.pauli_op.pauli_sum_op, 1.0, synthesis=self.synthesizer)

        if self.num_qubits == -1:
            num_qubits = evo_gate.num_qubits
            self.num_qubits = num_qubits
        # reset circuit everytime to avoid pile-up
        circ = QuantumCircuit(self.num_qubits)
        circ.append(evo_gate, list(range(self.num_qubits)))

        if optimize:
            assert self.circuit_optimizer is not None, \
                "Circuit to be optimized but not optimizer defined"
            circ = self.circuit_optimizer(circ)

        self.circuit = circ
        return self.circuit
