def heisenberg_xxz(
    qubits: int, coupling_field: float, external_field: float, normalize=False
) -> dict[str, float]:
    """
    One dimensional XXZ Heisenberg model parameterized by coupling field J,
    and external field h. The Hamiltonian is represented by:

    :math:`j sum_{<i, j>} (X_i, X_j + Y_i Y_j) + h sum_{<i, j>} (Z_i Z_j)

    Inputs:
        - qubits: Number of qubits for the Hamiltonian
        - j: Energy prefactor
        - h: External field

    Returns: Hamiltonian in dictionary form
    """

    if qubits <= 1:
        raise ValueError("Heisenberg XXZ model is not defined for one qubit")

    ham: dict[str, float] = {}
    i_n = ["i"] * qubits

    for i in range(qubits - 1):
        j = i + 1
        p_i = i_n

        p_i[i] = "x"
        p_i[j] = "x"
        ham["".join(p_i)] = coupling_field

        p_i[i] = "y"
        p_i[j] = "y"
        ham["".join(p_i)] = coupling_field

        p_i[i] = "z"
        p_i[j] = "z"
        ham["".join(p_i)] = external_field

        # Reset to avoid large copies
        p_i[i] = "i"
        p_i[j] = "i"

    if normalize:
        norm = sum(ham.values())
    else:
        norm = 1
    ham = {p: v / norm for p, v in ham.items()}
    return ham
