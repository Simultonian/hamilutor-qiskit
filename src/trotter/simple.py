from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.opflow import PauliTrotterEvolution, X, Y, Z, I  # For `eval`


def _circuit_eq(circuit1, circuit2) -> bool:
    # Conversion to Operator for the sake of checking equality
    Op1 = Operator(circuit1)
    Op2 = Operator(circuit2)

    return Op1.equiv(Op2)


def _qiskit_string_repr(h: dict[str, float]) -> str:
    # run eval on this string to attain `qiskit.opflow` object.
    new_terms = []
    for pauli, coeff in h.items():
        new_string = "^".join(pauli.upper())
        new_terms.append(f"{coeff} * ({new_string})")

    return " + ".join(new_terms)


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
    hamiltonian = eval(_qiskit_string_repr(h))

    # evolution operator
    evolution_op = ((t / reps) * hamiltonian).exp_i()

    # into circuit
    trotterized_op = PauliTrotterEvolution(trotter_mode="trotter", reps=reps).convert(
        evolution_op
    )

    return trotterized_op.to_circuit()
