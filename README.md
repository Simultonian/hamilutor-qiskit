A library built upon the qiskit framework to perform Hamiltonian simulations. This library further serves as an intermediate between qiskit and Menchbarker. [Qiskit](https://qiskit.org/) is an open-source SDK for working with quantum computers at the level of pulses, circuits, and application modules.

# Installation

The library is still in its early development and is not available as a package to install.

# Example

```python
from lietrotter import Lie

hamiltonian = "H2"
constructor = Lie()

constructor.load_hamiltonian(hamiltonian)
constructor.get_circuit()
dec_circuit = constructor.decompose_circuit()
depth = dec_circuit.depth()
print(f"depth: {depth}")
```

# Packaging

### Primary Modules

Consisting of simulation techniques, the core of Hamiltonian is divided into
independent modules that can each be used along with the secondary modules.
Currently, the following simulation techniques are supported:

- Trotterization

### Secondary Modules

On top of primary modules, secondary modules provide a layer of abstraction for
the users to use these simulation techniques for various different purposes.
These secondary modules can be used together to compare and choose
hamiltonian simulations specific to the task required. The planned secondary
modules will be of the following purpose:

- Comparison of methods
- Hamiltonian pre-processing & optimization
- Extrapolation of circuit properties
- Visualization
- Interface for running on different hardware

# Contribution Guidelines

For contributing please setup a venv and install [`requirements-dev.txt`](requirements-dev.txt).
The separation is to avoid users from installing unnecessary packages that are
only required for running checks locally. Ensure that the following standards
are met with before making a PR to avoid unnecessary load on CI.

## Formatting
All code must be formatted using `autopep8`. To check formatting, run:
```
./checks/flake8.sh
```

## Linter
The code is checked using `pylint` along with static typing supported by `mypy`.
The tests can be run by:
```
./checks/mypy.sh
./checks/pylint.sh
```

## Testing
Each new functionality must be supported with tests. Overall tests can be
performed by:
```
./checks/pytest.sh
```

# License

[Apache License 2.0](LICENSE.txt)
