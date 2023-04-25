from qiskit.quantum_info.operators.symplectic.random import random_pauli_list
import numpy as np


def random_hamiltonian(qubits: int, size: int, seed: int) -> dict[str, float]:
    np.random.seed(seed)

    pauli_strs = [
        str(x).lower() for x in random_pauli_list(qubits, size, seed, phase=False)
    ]
    coeffs = np.random.uniform(-1, 1, size)
    return {p: c for p, c in zip(pauli_strs, coeffs)}
