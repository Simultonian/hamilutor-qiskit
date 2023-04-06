from qiskit import QuantumCircuit


def circuit_constructor(gates_list: list[str], is_dag: bool = False) -> QuantumCircuit:
    """
    Constructs the circuit corresponding to the gates list given.

    Inputs:
        - gates_list: ith string represents the gates for ith qubit.

    Returns: QuantumCircuit for the given gates_list.
    """
    final_circ = QuantumCircuit(len(gates_list))
    for ind, gates in enumerate(gates_list):
        if is_dag:
            iterator = gates
        else:
            iterator = reversed(gates)

        for gate in iterator:
            match gate:
                case "h":
                    final_circ.h(ind)
                case "s":
                    if is_dag:
                        final_circ.sdg(ind)
                    else:
                        final_circ.s(ind)
                case "i":
                    break

    return final_circ
