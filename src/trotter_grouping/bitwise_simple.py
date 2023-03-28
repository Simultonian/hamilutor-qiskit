from qiskit import QuantumCircuit

from ..grouping.bitwise import (
    bitwise_group,
    bitwise_representor,
    bitwise_gate,
    bitwise_operator_convertor,
)

from ..trotter.simple import trotter


def _circuit_constructor(gates_list: list[str], is_dag: bool = False) -> QuantumCircuit:
    """
    Constructs the circuit corresponding to the gates list given.

    Inputs:
        - gates_list: ith string represents the gates for ith qubit.

    Returns: QuantumCircuit for the given gates_list.
    """
    final_circ = QuantumCircuit(len(gates_list))
    for ind, gates in enumerate(gates_list):
        if is_dag:
            iterator = gates
        else:
            iterator = reversed(gates)

        for gate in iterator:
            match gate:
                case "h":
                    final_circ.h(ind)
                case "s":
                    if is_dag:
                        final_circ.sdg(ind)
                    else:
                        final_circ.s(ind)
                case "i":
                    break

    return final_circ


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
    representor = bitwise_representor(list(h.keys()))

    # Getting the rotation and the anti-rotation circuit
    rot_circuit = _circuit_constructor(bitwise_gate(representor))
    anti_rot_circuit = _circuit_constructor(bitwise_gate(representor), True)

    # Rotating the operators and then using them in Trotter.
    rotated_operators = {}
    for pauli, coeff in h.items():
        coeff_c, new_pauli = bitwise_operator_convertor(pauli)
        rotated_operators[new_pauli] = coeff * coeff_c

    exp_circ = trotter(rotated_operators, t)

    final_circuit = rot_circuit.compose(exp_circ)
    final_circuit = final_circuit.compose(anti_rot_circuit)
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
    pauli_list = list(h.keys())

    if len(pauli_list) == 0:
        raise ValueError("Input Hamiltonian was empty.")

    # size of any pauli operator
    num_qubits = len(pauli_list[0])

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
