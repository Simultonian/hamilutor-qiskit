def ising_1d(qubits: int, energy_prefactor: float, external_field: float) -> dict[str, float]:
    """
    One dimensional Transverse-field Ising model parameterized by energy 
    prefactor J, and external field h. The Hamiltonian is represented by:

    :math:`j sum_{<i, j>} Z_i Z_j + h sum_i X`

    Inputs:
        - qubits: Number of qubits for the Hamiltonian
        - j: Energy prefactor
        - h: External field

    Returns: Hamiltonian in dictionary form
    """

    ham: dict[str, float] = {}
    i_n = ["i"] * qubits

    for i in range(qubits-1):
        j = i+1
        p_i = i_n.copy()
        p_i[i] = "z"
        p_i[j] = "z"
        ham["".join(p_i)] = energy_prefactor

    for i in range(qubits):
        p_i = i_n.copy()
        p_i[i] = "x"
        ham["".join(p_i)] = external_field

    norm = sum(ham.values())
    ham = {p:v/norm for p, v in ham.items()}
    return ham
