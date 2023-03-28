from qiskit import QuantumCircuit
from qiskit.opflow import PauliTrotterEvolution, X, Y, Z, I  # For `eval`
from ..utils.repr import qiskit_string_repr


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
