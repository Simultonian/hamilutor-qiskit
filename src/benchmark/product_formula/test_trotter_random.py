from ...hamiltonian import random_hamiltonian
from ..plot import plot_gate_count
from ...utils.gate_count import gate_count
from ..decompose import decompose

from ...trotter.simple import trotter
from ...qdrift.simple import qdrift


def test_trotter_random():
    qubits = 5
    num_terms = qubits**2
    ham = random_hamiltonian(qubits, num_terms, seed=42)

    trotter_circuit = decompose(trotter(ham))
    qdrift_circuit = decompose(qdrift(ham))

    trotter_gates = gate_count(trotter_circuit)
    qdrift_gates = gate_count(qdrift_circuit)

    fig = plot_gate_count([trotter_gates, qdrift_gates], ["simple trotter", "qdrift"])
    fig.write_image("simple_trotter.png")
