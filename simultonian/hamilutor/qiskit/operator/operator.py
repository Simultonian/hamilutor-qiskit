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
from qiskit.opflow import PauliSumOp  # type: ignore


class Hamiltonian(PauliSumOp):
    """
        Class for the Hamiltonian that must be manipulated before they are
        loaded into qiskit objects.

        These Hamiltonians will be loaded via Parser and manipulated using
        HamiltonianOptimizer subclasses. Further extensions for grouping
        algorithms will be added here.
    """
