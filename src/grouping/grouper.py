from abc import abstractmethod


class Grouper:
    """
    Abstract class for grouping algorithms.
    """

    def __init__(self, pauli_list: set[str]):
        self._commutable_sets = []

    @property
    def groups(self) -> list[set[str]]:
        return self._commutable_sets

    @abstractmethod
    def diagonalize(self, pauli_op: str) -> tuple[float, str]:
        """
        Gets the operator after it has been diagonlized by the circuit.
        """

    @abstractmethod
    def circuit(self, pauli_op: str) -> list[str]:
        """
        Calls the gate constructor with the representor string stored. This
        makes it easier for the user to access.
        """
