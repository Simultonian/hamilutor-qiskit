from qiskit import QuantumCircuit


def gate_count(circuit: QuantumCircuit):
    return dict(circuit.count_ops())
