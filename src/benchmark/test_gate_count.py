import pytest
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, CXGate
from .gate_count import gate_count


circuits = [
    [(HGate, [1]), (XGate, [1]), (CXGate, [0, 1])],
]

count_objs = [{"h": 1, "x": 1, "cx": 1}]

qubit_counts = [2]


@pytest.mark.parametrize("gates,count, qubit", zip(circuits, count_objs, qubit_counts))
def test_gate_count_simple(gates, count, qubit):
    circ = QuantumCircuit(qubit)
    for gate, qubits in gates:
        circ.append(gate(), qubits)
    result = gate_count(circ)

    assert result == count
