# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Dummy Hamiltonian Optimizer"""

from ..operator import Hamiltonian
from .baseoptimizer import Optimizer


class Dummy(Optimizer):
    """Dummy Optimizer that will just reverse the order of the Hamiltonian
       terms.
   """

    def __init__(self):
        super().__init__("DUMMY")

    def __call__(self, h: Hamiltonian):
        """Dummy Optimizer

        Return the same circuit

        Args:
            circuit: Circuit to be optimizer.
        Raises:
            AssertionError: circuit is not QuantumCircuit.
        """
        if not isinstance(h, Hamiltonian):
            raise ValueError("Incorrect type at dummy optimizer")
        reverse_permute = list(reversed(range(len(h))))
        h.permute(reverse_permute)
