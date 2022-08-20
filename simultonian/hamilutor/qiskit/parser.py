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
from typing import List
from qiskit.opflow import PauliSumOp  # type: ignore

from .operator import Hamiltonian
from ..baseparser import BaseParser


class Parser(BaseParser):
    """
        Parser to parse hamiltonians into qiskit objects.

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

    def parse_pauli(self, file_contents: str) -> Hamiltonian:
        """Parse given string

        Given string is formatted into a `PauliSumOp` given the format
        of the string is of `.pauli`.

        Args:
            - file_contents: string to parse
        Raises:
            - TypeError: File format is invalid.
        """
        lines = list(filter(lambda x: len(x) > 0, file_contents.splitlines()))
        pauli_pairs = []

        try:
            for line in lines:
                coeff, axis = line.split(" ")
                coeff = coeff.replace(" ", "").replace("i", "j")

                axis = axis.strip()
                pauli_pairs.append((axis, coeff))
        except TypeError as err:
            raise TypeError("Invalid file format") from err

        # TODO fix typing
        return Hamiltonian.from_list(pauli_pairs)  # type: ignore

    def __call__(self, file: str) -> PauliSumOp:
        """Parse given file

        Read the file and parse into a `PauliSumOp` if the format is
        acceptable.

        Args:
            - file: file name
        Raises:
            - TypeError: File format not supported.
        """
        extension, string = super().__call__(file)

        # since `pauli` is the only format.
        assert extension == "pauli"
        return self.parse_pauli(string)
