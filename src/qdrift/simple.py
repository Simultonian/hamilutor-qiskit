from qiskit import QuantumCircuit
from ..trotter import trotter_from_term
import numpy as np


def qdrift(h: dict[str, float], t: float = 1.0, eps: float = 1.0) -> QuantumCircuit:
    """
    API that takes Hamiltonian in a familiar format along with time and creates
    circuit that simulates the same using simple Trotterization.

    Input:
        - h: Hamiltonian in Pauli basis along with coefficients
        - t: Time
        - eps: Error factor for QDRIFT.
    Returns: Quantum Circuit for simulation
    """

    paulis = list(h.keys())
    num_qubits = len(paulis[0])
    coeffs = np.array([h[pauli] for pauli in paulis])
    weights = np.abs(coeffs)
    lambd = np.sum(weights)

    N = int(2 * (lambd**2) * (t**2) // eps)
    factor = lambd * t / N

    pauli_ops = [trotter_from_term((pauli, factor)) for pauli in paulis]
    sampled_inds = np.random.choice(len(pauli_ops), size=N, p=weights / lambd)
    sampled_terms = [pauli_ops[ind] for ind in sampled_inds]

    final_circuit = QuantumCircuit(num_qubits)

    for term in sampled_terms:
        final_circuit = final_circuit.compose(term)

    return final_circuit


def qdrift_error(h: dict[str, float], t: float, r: int) -> float:
    """
    API to determine the analytical error for the QDRIFT protocol based on the
    formula given in the arxiv submission.

    Input:
        - h: Hamiltonian in Pauli basis along with coefficients.
        - t: Time
        - r: The multiplicative factor w.r.t the number of terms in `h`.
    """
    l = len(h.keys())
    coeffs = np.array(h.values())
    weights = np.abs(coeffs)
    lambd = np.sum(weights)

    nr = (l**2) * (lambd**2) * (t**2)
    dr = 2 * r

    exp = np.exp(lambd * t * l / r)
    return nr * exp / dr
