from qiskit import QuantumCircuit
from .decompose import decompose
from ...utils import circuit_eq


def test_simple_decompose():
    circuit = QuantumCircuit(1)
    circuit.x(0)

    new_circuit = decompose(circuit)
    assert circuit_eq(new_circuit, circuit)
