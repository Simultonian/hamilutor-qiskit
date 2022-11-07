# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Lie Trotter functionality for constructing circuits."""
from qiskit import QuantumCircuit  # type: ignore

from .baseoptimizer import Optimizer


class Dummy(Optimizer):
    """Dummy Optimizer that will make no changes to the circuit.
    """

    def __init__(self):
        super().__init__("DUMMY")

    def __call__(self, circuit: QuantumCircuit):
        """Dummy Optimizer

        Return the same circuit

        Args:
            circuit: Circuit to be optimizer.
        Raises:
            AssertionError: circuit is not QuantumCircuit.
        """
        if not isinstance(circuit, QuantumCircuit):
            raise ValueError("Incorrect type at dummy optimizer")
        return circuit
