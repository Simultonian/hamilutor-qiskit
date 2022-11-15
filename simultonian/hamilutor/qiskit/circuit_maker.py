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
"""Base class for Circuit Maker."""

from qiskit import QuantumCircuit
from .sampler import Identity


class CircuitMaker:
    """
        CircuitMaker that constructs the circuit using the Pauli Sampler.
    """

    def __init__(
            self,
            method: str,
            num_qubits=-1):
        """
            Base class for all the `qiskit` methods that can construct a
            circuit out of a Hamiltonian.

            Args:
                - method: Method Name used for constructing the circuit
                - num_qubits: Number of qubits in the circuit construction
                - is_base: If the constructor is PauliSampler if
                           not then CircuitSampler.
        """
        self.method = method
        self.num_qubits: int = num_qubits

    def load(self, sampler: Identity) -> None:
        """Loading for the CircuitMaker would be equivalent of making the
           circuit.

        Args:
            - sampler: Sampler that will let the circuit maker get
            PauliSequences.
        """
        raise NotImplementedError("Can't make circuit using Base CircuitMaker")

    def roll(self) -> QuantumCircuit:
        raise NotImplementedError("Can't make circuit using Base CircuitMaker")
