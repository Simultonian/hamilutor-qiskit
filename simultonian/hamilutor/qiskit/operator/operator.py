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
from __future__ import annotations

from typing import Union

from qiskit.opflow import PauliSumOp  # type: ignore


class Hamiltonian:
    """
        Class for the Hamiltonian that must be manipulated before they are
        loaded into qiskit objects. These Hamiltonians will be loaded via
        Parser and manipulated using HamiltonianOptimizer subclasses. Further
        extensions for grouping algorithms will be added here.

        Args:
            dic: Decomposition of the operator in Pauli basis.

        Attributes:
            pauli_sum_op: qiskit object that will be used by qiskit circuit
                          constructors.

    """

    def __init__(
            self, op_iter: Union[dict[str, complex],
                                 list[tuple[str, complex]]]):
        if isinstance(op_iter, dict):
            self._raw: list[tuple[str, complex]] = list(op_iter.items())
        if isinstance(op_iter, list):
            self._raw = op_iter
        else:
            raise TypeError(
                "Incorrect input type provided for Hamiltonian init")

        self._pauli_op = PauliSumOp.from_list(op_iter)
        self._update = False

    @classmethod
    def from_dict(cls, op_dic: dict[str, complex]) -> 'Hamiltonian':
        """
        Construct `Hamiltonian` object from a dictionary of `Pauli -> coeff`.

        Args:
            dic: dictionary of Pauli operators and coefficients.
        """
        return cls(list(op_dic.items()))

    @classmethod
    def from_list(cls, op_list: list[tuple[str, complex]]) -> 'Hamiltonian':
        """
        Construct `Hamiltonian` object from a list of `(Pauli, coeff)`.

        Args:
            ls: List of Pauli operators and coefficients.
        """
        return cls(op_list)

    @property
    def pauli_sum_op(self) -> PauliSumOp:
        """
        Used for constructing circuit in qiskit, stores the Hamiltonian in
        `PauliSumOp` operator.
        """
        if not self._update:
            return self._pauli_op

        self._pauli_op = PauliSumOp.from_list(self._raw)
        self._update = False
        return self._pauli_op

    @pauli_sum_op.setter
    def pauli_sum_op(self, value: PauliSumOp) -> None:
        self._pauli_op = value
        self._update = False

    def permute(self, permutation: list[int]) -> None:
        """
        Permute the ordering of the terms in Hamiltonian.

        Args:
            permutation: List of indices to be ordered.
        """
        new_list = []
        for ind in permutation:
            new_list.append(self._raw[ind])

        self._raw = new_list
        self._update = True

    def swap(self, swap_map: dict[int, int]) -> None:
        """
        Swap the ordering of the terms in Hamiltonian.

        Args:
            swap_map: Mapping from indices that are to be swapped.
        """
        for original, new in swap_map.items():
            self._raw[original], self._raw[new] = \
                self._raw[new], self._raw[original]

        self._update = True

    def truncate(self, deletion: set[int]) -> None:
        """
        Truncate the terms in the Hamiltonian.

        Args:
            deletion: Set of indices to remove.
        """
        new_raw = [pauli_pair for ind, pauli_pair in enumerate(
            self._raw) if ind not in deletion]

        self._raw = new_raw
        self._update = True
