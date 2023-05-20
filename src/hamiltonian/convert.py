from qiskit.quantum_info import SparsePauliOp


def to_pauli_op(hamiltonian: dict[str, float]):
    """
    Converts the dictionary format to Pauli operator.

    Inputs:
        - hamiltonian: Hamiltonian in Pauli basis

    Returns: SparsePauliOp object
    """

    if len(hamiltonian) == 0:
        raise ValueError("Invalid Hamiltonian, no Pauli elements found")

    paulis, coeffs = list(zip(*hamiltonian.items()))

    paulis = list(paulis)

    paulis = [pauli.upper() for pauli in paulis]

    op = SparsePauliOp(paulis, coeffs)
    return op
