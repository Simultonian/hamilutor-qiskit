def commutes(pauli_list, pauli_a) -> bool:
    """
        Checks if the given pauli operator commutes with the rest of the
        elements in the set.
    """
    for pauli_b in pauli_list:
        for a, b in zip(pauli_a, pauli_b):
            if (a == b) or (a == "i") or (b == "i"):
                continue
            return False
    return True

def bitwise_group(pauli_list: list[str]) -> list[list[str]]:
    """Creating the pauli groups as a list of strings.
    Input:
        - pauli_list: List of strings representing the pauli operator.

    Returns: List of lists, each forming a set of commuting pauli operators.
    """
    groups = []
    for pauli in pauli_list:
        for group in groups:
            if commutes(group, pauli):
                group.append(pauli)
                break
        else:
            groups.append([pauli])
    return groups
