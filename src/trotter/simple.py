from qiskit import QuantumCircuit
from qiskit.opflow import PauliTrotterEvolution, X, Y, Z, I  # For `eval`
from ..utils.repr import qiskit_string_repr, qiskit_string_repr_pauli


def trotter_from_terms(terms: list[tuple[str, float]]) -> QuantumCircuit:
    """
    API that takes a list of terms that must be exponentiated in the specific
    order, that may or may not have repetitions. The coefficients are assumed
    to already account the time scaling.

    Input:
        - terms: list of pairs of pauli operator and the coefficient.
    Returns: Quantum Circuit with exponentiation in the defined ordered.
    """
    num_qubits = len(terms[0][0])
    final_circuit = QuantumCircuit(num_qubits)

    for term in terms:
        final_circuit = final_circuit.compose(trotter_from_term(term))

    return final_circuit

def trotter_from_term(term: tuple[str, float]) -> QuantumCircuit:
    pauli_op = eval(qiskit_string_repr_pauli(term))
    evolution_op = pauli_op.exp_i()
    trotterized_op = PauliTrotterEvolution(trotter_mode="trotter").convert(
        evolution_op
    )
    return trotterized_op.to_circuit()


def trotter(h: dict[str, float], t: float = 1.0, reps: int = 1) -> QuantumCircuit:
    """
    API that takes Hamiltonian in a familiar format along with time and creates
    circuit that simulates the same using simple Trotterization.

    Input:
        - h: Hamiltonian in Pauli basis along with coefficients
        - t: Time
        - reps: The number of times to repeat trotterization steps.
    Returns: Quantum Circuit for simulation
    """
    hamiltonian = eval(qiskit_string_repr(h))

    # evolution operator
    evolution_op = ((t / reps) * hamiltonian).exp_i()

    # into circuit
    trotterized_op = PauliTrotterEvolution(trotter_mode="trotter", reps=reps).convert(
        evolution_op
    )

    return trotterized_op.to_circuit()
