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
from qiskit.synthesis import LieTrotter
from ..constructor import Constructor


class Lie(Constructor):
    """Lie Trotter method
    """

    def __init__(self, optimizer=None, num_qubits: int = -1, order: int = 1):
        super().__init__("SUZUKI", optimizer, num_qubits)

        assert order > 0, "Incorrect order."
        self.order = order

        self.re_init()

    def re_init(self, _reps: int = 1):
        """Re-initialize synthesizer
        Re-initializes the synthesizer with new number of reps.

        Args:
            _reps: Number of times QDRIFT must be repeated in the circuit.
        Raises:
            AssertionError: Incorrect rep count.
            AssertionError: QDrift could not construct circuit.
        """
        assert _reps > 0, "Incorrect number of reps provided"
        self.synthesizer = LieTrotter(reps=_reps)
        assert self.synthesizer is not None, "Error constructing the circuit."
