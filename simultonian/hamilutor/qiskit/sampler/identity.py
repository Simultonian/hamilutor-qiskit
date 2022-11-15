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
"""Identity Distribution of Hamiltonian that does not do optimizations"""
from __future__ import annotations

from typing import Any, Iterable, Optional
from qiskit.opflow import PauliSumOp  # type: ignore
from ..parser import PauliSequencesList, PauliSequence


class Identity:
    """
        Identity Hamiltonian that will apply no optimization and pass on the
        parsed values as they are.

        Attributes:
            pauli_sum_op: qiskit object that will be used by qiskit circuit
                          constructors.

    """

    def __init__(self):
        # If the attribute is True then there is a need for update
        self._pauli_op_update = False
        self._data: PauliSequencesList = []
        self._pauli_op: Optional[PauliSumOp] = None

    @property
    def data(self) -> PauliSequencesList:
        return self._data

    @data.setter
    def data(self, value: PauliSequencesList) -> None:
        raise AttributeError("Data can't be set.")

    @property
    def pauli_op(self) -> PauliSumOp:
        """
        Used for constructing circuit in qiskit, stores the Hamiltonian in
        `PauliSumOp` operator.
        """
        if not self._pauli_op_update:
            if self._pauli_op is None:
                raise AttributeError("update set to False but no pauli_op.")
            return self._pauli_op

        # since the elements are list of paulis themselves
        flattened_op = [
            pauli for pauli_set in self._data for pauli in pauli_set]

        self._pauli_op = PauliSumOp.from_list(flattened_op)
        self._update = False

        return self._pauli_op

    @pauli_op.setter
    def pauli_op(self, value: Any) -> None:
        raise AttributeError("Pauli operator can't be set.")

    def __len__(self) -> int:
        """
        Represents the number of PauliSequence rather than the number of
        Pauli terms.
        """
        return len(self._data)

    def load(self, data: PauliSequencesList) -> None:
        """
        Loads Data into the Sampler, this only copies the data into the class
        attribute.

        Attributes:
            - parser: Parser instance that has the required data loaded.
        """
        self._data = data

    def roll(self) -> PauliSequencesList:
        """Roll the Data

        All the parsed data will be rolled forward to the caller.

        Returns:
            - Pauli pair
        """
        return self.data

    def sample(self) -> Iterable[PauliSequence]:
        """Sample Paulis

        Samples the Pauli elements from the Parsed file. The samples are
        present in order and are only repeated once all the elements are
        exhausted.

        Returns:
            - Iterable of PauliRaw
        """
        for pauli in self.data:
            yield pauli
