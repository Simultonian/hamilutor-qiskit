import json


def save_hamiltonian(ham: dict[str, float], file: str):
    try:
        with open(file, "w") as outfile:
            json.dump(ham, outfile)
    except FileNotFoundError:
        raise ValueError("File not found")
    except Exception as e:
        raise e


def load_hamiltonian(file: str) -> dict[str, float]:
    try:
        with open(file, "r") as infile:
            return json.load(infile)
    except json.JSONDecodeError as e:
        raise ValueError("Incorrect format")
    except FileNotFoundError:
        raise ValueError("File not found")
    except Exception as e:
        raise e
