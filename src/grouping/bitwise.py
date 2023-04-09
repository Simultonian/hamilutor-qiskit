from .grouper import Grouper
from ..utils import get_el


class Bitwise(Grouper):
    """
    A class that will contain the bitwise grouping information for a single
    Hamiltonian. This will make it easier to use and will reduce overhead cost
    of calculating things repetitively. The original API will be allowed in use
    in parallel in case the application does not need the entire functionality.
    """

    def __init__(self, pauli_list: set[str]):
        self._commutable_sets = bitwise_group(pauli_list)
        self.map_repr: dict[str, str] = {}

        for comm_set in self._commutable_sets:
            bitwise_repr = bitwise_representor(comm_set)
            for pauli in comm_set:
                self.map_repr[pauli] = bitwise_repr

    def diagonalize(self, pauli_op: str) -> tuple[float, str]:
        """
        Gets the operator after it has been diagonlized by the circuit.
        """
        return bitwise_operator_convertor(pauli_op)

    def circuit(self, pauli_op: str) -> list[str]:
        """
        Calls the gate constructor with the representor string stored. This
        makes it easier for the user to access.
        """
        return bitwise_gate(self.map_repr[pauli_op])


def commutes(pauli_list: set[str], pauli_a: str) -> bool:
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


def bitwise_group(pauli_list: set[str]) -> list[set[str]]:
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


def bitwise_representor(pauli_list: set[str]) -> str:
    """
    Get the Pauli string that represents the entire commuting Pauli set, we
    construct this by taking the preferred Pauli operator for each position,
    where `i` is below `x`, `y`, and `z` which are at equal level.

    To be in the same bitwise commuting group, there can only be one dominant
    Pauli operator.

    Input:
        - pauli_list: List of Pauli operators that are commutable.

    Returns: Representor string of the group.

    Raises:
        - ValueError: if the list is empty.
    """
    if len(pauli_list) == 0:
        raise ValueError("Empty Group, no representation can be made.")

    x = get_el(pauli_list)

    repr_str = ["i"] * len(x)

    for pauli in pauli_list:
        for i, a in enumerate(pauli):
            if a != "i":
                repr_str[i] = a

    return "".join(repr_str)


DIAGONAL_GATES = {
    "i": "i",
    "x": "h",
    "y": "hs",
    "z": "i",
}

DIAGONAL_PAULIS = {
    "i": (1.0, "i"),
    "x": (1.0, "z"),
    "y": (-1.0, "z"),
    "z": (1.0, "z"),
}


def bitwise_gate(repr_str: str) -> list[str]:
    """
    Given Pauli representor string, we return the set of gates for each
    position that will diagonalize all the Pauli operators in the commutable
    set represented by the representor string.

    Input:
        - repr_str: representor string
    Returns: List of gates for each qubit position.
    """
    return [DIAGONAL_GATES[x] for x in repr_str]


def bitwise_operator_convertor(pauli: str) -> tuple[float, str]:
    """
    Given the Pauli operator, the return value represents the Pauli operator
    that we will obtain after the operator has been diagonalized.

    Input:
        - pauli: Pauli operator that has to be diagonaized.
    Return: New operator along with the coefficient after diagonalized.

    Raises:
        - ValueError: If the supplied string is empty
    """
    if len(pauli) == 0:
        raise ValueError("Empty Pauli operator supplied for bitwise conversion.")

    coeff = 1.0
    pauli_new = []

    for p in pauli:
        c, p_new = DIAGONAL_PAULIS[p]
        coeff *= c
        pauli_new.append(p_new)

    return (coeff, "".join(pauli_new))
