from qiskit import QuantumCircuit
from .simple import qdrift
import numpy as np


def gdrift(h: dict[str, float], t: float = 1.0, eps:float = 1.0) -> QuantumCircuit:
    """
    API for combinining Pauli grouping and QDRIFT.

    Input:
        - h: Hamiltonian in Pauli basis along with coefficients
        - t: Time
        - eps: Error factor for QDRIFT.
    Returns: Quantum Circuit for simulation
    """

    return qdrift(h, t, eps)
