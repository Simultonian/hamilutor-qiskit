Library to run Hamiltonian Simulations on qiskit using different techniques for
the sake of analyzing and benchmarking.


## Pauli Grouping
Bitwise Pauli grouping has been implemented in `src/grouping/bitwise.py` that 
contains the functionality for grouping Pauli operators and constructing the 
gates that will diagonalize the given Commutable set of Pauli operators.

## Troterrization
To implement simple Trotterization technique that will take a Hamiltonian `H` 
in the form of `list[tuple[float, str]]` and time `t` and product `e^{-itH}`.

For the sake of this module, we will be using qiskit for creating circuits. The
implementation is present in `src/trotter/simple.py`
