from typing import Callable
from qiskit import QuantumCircuit

from ..grouping.grouper import Grouper

from ..trotter.simple import trotter_from_terms

from ..utils import circuit_constructor, get_el


def generic(
    grouper_class: Callable[[set[str]], Grouper],
    orderer: Callable[[set[str]], list[str]],
    h: dict[str, float],
    t: float = 1.0,
    reps: int = 1,
) -> QuantumCircuit:
    """
    A generic trotterization constructor.

    Inputs:
        - grouper: Pauli grouper
        - orderer: Function that orders the diagonalized terms
        - h: Hamiltonian in dictionary form
        - t: Float representing time of evolution
        - reps: Repetitions for Trotterization.
    Returns: QuantumCircuit that will simulate the Hamiltonian
    """
    pauli_list = set(h.keys())

    if len(pauli_list) == 0:
        raise ValueError("Input Hamiltonian was empty.")

    # size of any pauli operator
    first = get_el(pauli_list)
    num_qubits = len(first)

    grouper = grouper_class(pauli_list)
    groups = grouper.groups
    group_circs = []

    # Get relevant circuits for all the groups
    for group in groups:
        pauli = get_el(group)

        # Diagonalizing circuits
        diag_circ = circuit_constructor(grouper.circuit(pauli))
        diag_circ_c = diag_circ.inverse()

        # Setting the order according to ordere
        ordered = orderer(group)
        ordered_tuples = []
        for p in ordered:
            coeff, term = grouper.diagonalize(p)
            coeff = (t / reps) * h[p] * coeff
            ordered_tuples.append((term, coeff))

        # time will be scaled down by reps
        exp_circ = trotter_from_terms(ordered_tuples)

        final_circuit = QuantumCircuit(num_qubits)

        # TODO: Issue 30
        # Combining the three sections
        final_circuit = diag_circ.compose(exp_circ)
        final_circuit = final_circuit.compose(diag_circ_c)
        group_circs.append(final_circuit)

    final_circuit = QuantumCircuit(num_qubits)
    for _ in range(reps):
        for group_circ in group_circs:
            final_circuit = final_circuit.compose(group_circ)

    return final_circuit
