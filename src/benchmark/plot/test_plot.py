from .plot import plot_gate_count, plot_circuit_depth

count_list = [
    {"h": 1, "x": 1, "cx": 1},
    {"h": 0, "x": 4, "cx": 4},
]

methods = ["trotter", "qdrift"]


def test_gate_count_simple():
    """
    Test to see if the functionality runs without crashing.
    """
    _ = plot_gate_count(count_list, methods)


gate_depth = [10, 20]


def test_circuit_depth_simple():
    """
    Test to see if the functionality runs without crashing.
    """
    _ = plot_circuit_depth(gate_depth, methods)
