# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Hamiltonian Optimizer testing."""

import pytest

from simultonian.hamilutor.qiskit import Lie
from simultonian.hamilutor.qiskit.hamiltonian_optimizer import Dummy


@pytest.mark.parametrize(['h_str'], [("""1 Z\n1 X""",)])
def test_dummy_same_constructor(h_str: str):
    """
    Validity of Hamiltonian after reversing the order.
    """
    h_optimizer = Dummy()
    lie = Lie()
    lie.load_hamiltonian_string(h_str)

    assert lie.pauli_op is not None, "Pauli Op does not exist."

    raw_init = lie.pauli_op._raw

    lie.optimize_hamiltonian(h_optimizer)

    raw_new = lie.pauli_op._raw

    for old, new in zip(raw_init, reversed(raw_new)):
        assert old == new, "Incorrect Ordering"
