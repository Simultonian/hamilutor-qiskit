from .port import save_hamiltonian, load_hamiltonian
import os

def test_load_save():
    file_name = "file.json"
    ham = {"x": 1.0, "z": -1.0}
    save_hamiltonian(ham, file_name)
    result = load_hamiltonian(file_name)
    os.remove(file_name)
    assert ham == result
