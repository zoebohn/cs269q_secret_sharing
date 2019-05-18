from pyquil import Program
from pyquil.gates import CNOT, CZ, H, X, Z
import random
from pyquil.api import QVMConnection

def choose_random_direction():
    x_or_y = random.getrandbits(1)
    if x_or_y == 1:
        return 'x'
    else:
        return 'y'

def alice(qubit, message, program):
    alice_measure_dir = choose_random_direction()
    # TODO
    return alice_measure_dir

def bob(qubit, program):
    bob_measure_dir = choose_random_direction()
    # TODO
    return bob_measure_dir

def charlie(qubit, program):
    charlie_measure_dir = choose_random_direction()
    # TODO 
    return charlie_measure_dir

def check_directions(alice_measure_dir, bob_measure_dir, charlie_measure_dir):
    pass

def bob_and_charlie(bob_measure_result, charlie_measure_result):
    pass 

# from docs.rigetti.com
def ghz_state(qubits, program):
    program += H(qubits[0])
    for q1, q2 in zip(qubits, qubits[1:]):
        program += CNOT(q1, q2)
    return program

def initial_setup():
    message = random.getrandbits(MSG_LENGTH)
    
    alice_qubits = []
    bob_qubits = []
    charlie_qubits = []
    
    program = Program()
    
    # entangle qubits (GHZ)
    for q in range(0, MSG_LENGTH, 3):
        alice_qubits.append(q)
        bob_qubits.append(q + 1)
        charlie_qubits.append(q + 2)
        program = ghz_state([q, q + 1, q + 2], program)

    return alice_qubits, bob_qubits, charlie_qubits, message, program

MSG_LENGTH = 1 #@Emma: might have to tweak below code for longer messages to retry individual qubits rather than all of the qubits if 
NUM_TRIALS = 1
retries = 0
for trial in range(NUM_TRIALS):
    alice_q, bob_q, charlie_q, message, program = initial_setup()

    # perform secret sharing procedure once per message bit
    for i in range(MSG_LENGTH):
        while (True): # retry until success
            alice_measure_dir = alice(alice_q[i], message, program)
            bob_measure_dir = bob(bob_q[i], program)
            charlie_measure_dir = charlie(charlie_q[i], program)
            should_abort = check_directions(alice_measure_dir, bob_measure_dir, charlie_measure_dir)
            if should_abort:
                print("Abort! Measurements yielded no useful information. Retrying...") 
                retries += 1
                continue
            # run program, now that we know results will be interesting
            qvm = QVMConnection()
            program = program.measure_all() # TODO - this is just measuring them all, not according to a particular direction
            results = qvm.run(program)[0]
            alice_measure_result = results[0]
            bob_measure_result = results[1]
            charlie_measure_result = results[2]

            joint_result = bob_and_charlie(bob_measure_result, charlie_measure_result)
            if joint_result == alice_measure_result:
                print("Success! Bob and Charlie reconstructed one bit of the secret message.")
                break
            else:
                print("Failure! Bob and Charlie reconstructed an incorrect bit of the secret message.")
                exit() # end proram, we have a bug

    print("Bob and Charlie succeeded with " + str(retries) + " retries.")

    




