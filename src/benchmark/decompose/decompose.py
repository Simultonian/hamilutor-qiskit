from qiskit import QuantumCircuit
from qiskit.compiler import transpile


DEFAULT_GATES = ["rz", "h", "s", "cx", "cz"]


def decompose(circ: QuantumCircuit, basis=None) -> QuantumCircuit:
    if basis is None:
        basis = DEFAULT_GATES

    return transpile(circ, basis_gates=basis)
