from qiskit import QuantumCircuit

from ..grouping.bitwise import Bitwise

from .group_trotter import generic
from ..ordering import lexico


def bitwise_simple(
    h: dict[str, float], t: float = 1.0, reps: int = 1
) -> QuantumCircuit:
    """
    Takes in a Hamiltonian and constructs the simple Trotterization circuit
    after grouping the terms using bitwise Pauli grouping.

    Inputs:
        - h: Hamiltonian in dictionary form.
        - t: Float representing time of evolution.
        - reps: Repetitions for Trotterization.
    Returns: QuantumCircuit that will simulate the Hamiltonian
    """
    return generic(Bitwise, lexico, h, t, reps)
