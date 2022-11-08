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
"""Base class for Hamiltonian optimizer."""

from ..operator import Hamiltonian


class Optimizer:

    def __init__(self, name: str = "base"):
        """
            Base Class for optimizer that makes changes to Hamiltonian.
            These optimizers can be treated as passes that can be used in
            sequence.

            Args:
                - name: Name of optimization
        """
        self.name = name

    def __call__(self, h: Hamiltonian):
        """
        Run the optimization on the given Hamiltonian. The changes are made
        in-place so no value is returned.
        """
        raise NotImplementedError(
            "Accessing superclass for optmizer is not allowed")
