from qiskit.quantum_info import Operator

def circuit_eq(circuit1, circuit2) -> bool:
    # Conversion to Operator for the sake of checking equality
    Op1 = Operator(circuit1)
    Op2 = Operator(circuit2)

    return Op1.equiv(Op2)
