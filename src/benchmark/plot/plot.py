import plotly.express as px


def _plot_bar(plot_dict: dict[str, int], x_val: str, y_vals: list[str]):
    fig = px.bar(
        data_frame=plot_dict,
        x=x_val,
        y=y_vals,
        opacity=0.9,
        orientation="v",
        barmode="group",
    )
    return fig


def plot_gate_count(gate_counts: list[dict[str, int]], methods: list[str]):
    """
    Plots bar graphs to compare the gate count of each method. The user has to
    pass a list of dictionaries which indicate gate count of each gate. They
    also have to pass a list of methods each of these gate counts represent
    for naming.

    Inputs:
        - gate_counts: Dictionaries representing gate counts
        - methods: List of strings naming each method
    Returns: Figure for bar chart
    """

    gates = set()
    for count in gate_counts:
        gates.update(count.keys())

    counts = {gate: [] for gate in gates}
    for count in gate_counts:
        for gate in gates:
            if gate not in counts:
                counts[gate].append(0)
            else:
                counts[gate].append(count[gate])

    if len(methods) == 0:
        counts["method"] = [f"{ind}" for ind in range(len(gate_counts))]
    else:
        counts["method"] = methods

    return _plot_bar(counts, "method", list(gates))


def plot_circuit_depth(depths: list[int], methods: list[str]):
    """
    Plot bar chart for circuit depth, the user passes a list of natural numbers
    along with list of strings naming the method.

    Inputs:
        - depths: List of integers representing depths of circuits
        - methods: List of strings naming each method

    Returns: Figure for bar chart
    """
    counts = {"depth": depths, "methods": methods}
    return _plot_bar(counts, "methods", ["depth"])
