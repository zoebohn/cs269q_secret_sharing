from pyquil import Program
from pyquil.gates import CNOT, CZ, H, X, Z

def Alice(qubits, message):
    pass

def Bob(qubits):
    pass

def Charlie(qubits):
    pass

# from docs.rigetti.com
def ghz_state(qubits):
    program = Program()
    program += H(qubits[0])
    for q1, q2 in zip(qubits, qubits[1:]):
        program += CNOT(q1, q2)
    return program

def initial_setup():
    pass




