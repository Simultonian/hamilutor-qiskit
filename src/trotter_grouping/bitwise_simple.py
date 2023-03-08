from qiskit import QuantumCircuit

from ..grouping.bitwise import (
    bitwise_group,
)

from ..trotter.simple import trotter


def bitwise_simple(h: dict[str, float], t: float = 1.0) -> QuantumCircuit:
    """
    Takes in a Hamiltonian and constructs the simple Trotterization circuit
    after grouping the terms together.

    Inputs:
        - h: Hamiltonian in dictionary form.
        - t: float representing time of evolution.
    """
    pauli_list = list(h.keys())

    if len(pauli_list) == 0:
        raise ValueError("Input Hamiltonian was empty.")

    # size of any pauli operator
    num_qubits = len(pauli_list[0])

    groups = bitwise_group(pauli_list)
    grouped_hs = [{pauli: h[pauli] for pauli in group} for group in groups]

    trotter_circs = [trotter(h_i, t) for h_i in grouped_hs]
    final_circuit = QuantumCircuit(num_qubits)

    for circ in trotter_circs:
        final_circuit = final_circuit.compose(circ)

    return final_circuit
