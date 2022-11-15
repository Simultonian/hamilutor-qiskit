# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=fixme
"""Base class for Parser across frameworks"""
from typing import Iterable, List, Tuple

from ..baseparser import BaseParser

PauliRaw = Tuple[str, complex]
PauliSequence = List[PauliRaw]

"""
Type for the unit of manipulation in the sampler
"""
PauliSequencesList = List[PauliSequence]


class Parser(BaseParser):
    """
        Sampler that will load the file and serves as a distribution for
        the Hamiltonian terms.

        =================
        Formats supported
        =================

        The format of the file is decided based on the extension of the file.
        Incorrect format will throw error.

        ---------------
        `.pauli` format
        ---------------
        Format that is specific to Simultonian, the file must contain
        coefficients followed by the Pauli operators. A sample format has been
        given:
        ```
        0.5 XYZIX
        -0.5i IIIXY
        ```
        Note that both `i` and `j` are supported.
    """

    def __init__(self) -> None:
        super().__init__("qiskit")
        self.formats: List[str] = ["pauli"]
        self._data: PauliSequencesList = []

    @property
    def data(self) -> PauliSequencesList:
        return self._data

    @data.setter
    def data(self, _new_data):
        raise AttributeError("Data of Parser can only be read.")

    def load(self, string: str, is_file: bool = False) -> None:
        """Parse

        The given string can either be a file or the content itself that must
        be parsed. This will be judged based on the value given to `is_file`.

        Args:
            - string: string that represents the file name or content.
            - is_file: value that will determine if the string given is file
                       name or content.
        Raises:
            - TypeError: File format is invalid.
            - NotImplementedError: File extension is not supported in the lib.
        """
        if is_file:
            extension, content = self.base_parse(string)

            # since `pauli` is the only format.
            assert extension == "pauli"
            self.parse_pauli(content)
        else:
            self.parse_pauli(string)

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

    def parse_pauli(self, file_contents: str) -> None:
        """Parse given string

        Given string is formatted into [Pauli, coeff] format.

        Args:
            - file_contents: string to parse
        Raises:
            - TypeError: File format is invalid.
        """
        lines = list(filter(lambda x: len(x) > 0, file_contents.splitlines()))
        pauli_pairs = []

        try:
            for line in lines:
                _coeff, axis = line.split(" ")
                coeff = complex(_coeff.replace(" ", "").replace("i", "j"))

                axis = axis.strip()
                pauli_pairs.append([(axis, coeff)])
        except TypeError as err:
            raise TypeError("Invalid file format") from err

        self._data = pauli_pairs
