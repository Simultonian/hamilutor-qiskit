def qiskit_string_repr(h: dict[str, float]) -> str:
    # run eval on this string to attain `qiskit.opflow` object.
    new_terms = []
    for pauli, coeff in h.items():
        new_string = "^".join(pauli.upper())
        new_terms.append(f"{coeff} * ({new_string})")

    return " + ".join(new_terms)


def qiskit_string_repr_pauli(term: tuple[str, float]) -> str:
    # run eval on this string to attain `qiskit.opflow` object.
    pauli, coeff = term
    new_string = "^".join(pauli.upper())
    return f"{coeff} * ({new_string})"
