def lexico(ops: set[str]) -> list[str]:
    """
    The given operators that are diagonalized already will be ordered qubitwise
    which comes out to be same strategy as lexicographic ordering.
    """
    return sorted(ops)
