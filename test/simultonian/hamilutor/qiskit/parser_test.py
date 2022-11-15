# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Simple tests for testing the parsing capacity of `Parser`"""

import os
from typing import List, Tuple

import pytest
from testfixtures import TempDirectory  # type: ignore

from simultonian.hamilutor.qiskit import Parser


@pytest.mark.parametrize(['string', 'pauli_set'], [
    ("""-0.2 ZI\n-0.1 IX""",
     {("ZI", complex(-0.2, 0)), ("IX", complex(-0.1, 0))}),
    ("""-0.2j ZI\n-0.1 IX""",
     {("ZI", complex(0, -0.2)), ("IX", complex(-0.1, 0))}),
    ("""-0.2i ZI\n-0.1 IX""",
     {("ZI", complex(0, -0.2)), ("IX", complex(-0.1, 0))})
])
def test_hamiltonian(string: str, pauli_set: List[Tuple[str, complex]]):
    """
    Checks if the qiskit parser is able to load a hamiltonian
    """
    parser = Parser()
    file_name = "test_hamiltonian.pauli"

    with TempDirectory() as temp_dir:
        temp_dir.write(file_name, string.encode())
        assert temp_dir.path is not None

        new_file_name = os.path.join(temp_dir.path, file_name)

        parser.load(str(new_file_name), True)

    # Checking roll
    result = parser.roll()
    for pauli in result:
        # The return value is a list with one element
        assert pauli[0] in pauli_set

    # Checking sample
    for pauli in parser.sample():
        assert pauli[0] in pauli_set
