from typing import Callable
from qiskit import QuantumCircuit

from ..grouping.bitwise import (
    bitwise_group,
    bitwise_representor,
    bitwise_gate,
    bitwise_operator_convertor,
)

from ..grouping.grouper import Grouper

from ..trotter.simple import trotter

from ..utils import circuit_constructor, get_el


def group_trotter(h: dict[str, float], t: float = 1.0) -> QuantumCircuit:
    """
    Runs simple Trotter for the case where all the elements of the Hamiltonian
    are commuting Pauli operators. It uses rotation and exponentiation.

    Inputs:
        - h: Hamiltonian in dictionary form.
        - t: Float representing time of evolution.
    Returns: QuantumCircuit that will simulate the Hamiltonian
    """

    # Getting the group representation
    representor = bitwise_representor(set(h.keys()))

    # Getting the rotation and the anti-rotation circuit
    rot_circuit = circuit_constructor(bitwise_gate(representor))
    anti_rot_circuit = circuit_constructor(bitwise_gate(representor), True)

    # Rotating the operators and then using them in Trotter.
    rotated_operators = {}
    for pauli, coeff in h.items():
        coeff_c, new_pauli = bitwise_operator_convertor(pauli)
        rotated_operators[new_pauli] = coeff * coeff_c

    exp_circ = trotter(rotated_operators, t)

    final_circuit = rot_circuit.compose(exp_circ)
    final_circuit = final_circuit.compose(anti_rot_circuit)
    return final_circuit


def generic(
    grouper: Grouper,
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

    grouper = Grouper(pauli_list)
    groups = grouper.groups
    group_circs = []

    # Get relevant circuits for all the groups
    for group in groups:
        pauli = get_el(group)
        diag_circ = circuit_constructor(grouper.circuit(pauli))
        diag_circ_c = diag_circ.inverse()

        diag_ham = {}
        for p in group:
            coeff, term = grouper.diagonalize(p)
            diag_ham[term] = h[p] * coeff

        # time will be scaled down by reps
        exp_circ = trotter(diag_ham, t / reps)

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


def bitwise_simple(
    h: dict[str, float], t: float = 1.0, reps: int = 1
) -> QuantumCircuit:
    """
    Takes in a Hamiltonian and constructs the simple Trotterization circuit
    after grouping the terms together.

    Inputs:
        - h: Hamiltonian in dictionary form.
        - t: Float representing time of evolution.
        - reps: Repetitions for Trotterization.
    Returns: QuantumCircuit that will simulate the Hamiltonian
    """
    pauli_list = set(h.keys())

    if len(pauli_list) == 0:
        raise ValueError("Input Hamiltonian was empty.")

    # size of any pauli operator

    first = ""
    for x in pauli_list:
        first = x
        break

    num_qubits = len(first)

    groups = bitwise_group(pauli_list)
    grouped_hs = [{pauli: h[pauli] for pauli in group} for group in groups]

    # Using rotation and anti-rotation functionality, time must be divided
    trotter_circs = [group_trotter(h_i, t / reps) for h_i in grouped_hs]
    final_circuit = QuantumCircuit(num_qubits)

    # Repeating
    for _ in range(reps):
        for circ in trotter_circs:
            final_circuit = final_circuit.compose(circ)

    return final_circuit
