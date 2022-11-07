# This code is part of Simultonian
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
    circuit_optimizer is a sub-module that will take in circuits and optimize
    them using qiskit functionality.
"""

from .baseoptimizer import CircuitOptimizer
from .dummyoptimizer import Dummy

__all__ = ["Dummy", "CircuitOptimizer"]
