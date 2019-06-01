from pyquil import Program
from pyquil.noise import add_decoherence_noise
from pyquil.gates import CNOT, H, S
import random
from pyquil.api import QVMConnection
from pyquil.api import WavefunctionSimulator
from pyquil.api import get_qc

def choose_random_direction():
    x_or_y = random.getrandbits(1)
    if x_or_y == 1:
        return 'x'
    else:
        return 'y'

# TODO - somewhat unsure of this
    # measuring in x direction means applying an H gate
    # measuring in the y direction means apply an H gate followed by an S_dagger gate
    # (view in chrome): https://docs.microsoft.com/en-us/quantum/concepts/pauli-measurements?view=qsharp-preview
def prepare_measurement(qubit, direction, program):
    if direction == 'x':
        program += H(qubit)
    else:
        program += H(qubit)
        program_S_dagger = Program()
        program_S_dagger += S(qubit)
        program += program_S_dagger.dagger()

    return program

# TODO - how to incorporate message?
def alice(qubit, program):
    alice_measure_dir = choose_random_direction()
    program = prepare_measurement(qubit, alice_measure_dir, program)
    return alice_measure_dir, program

def bob(qubit, program):
    bob_measure_dir = choose_random_direction()
    program = prepare_measurement(qubit, bob_measure_dir, program)
    return bob_measure_dir, program

def charlie(qubit, program):
    charlie_measure_dir = choose_random_direction()
    program = prepare_measurement(qubit, charlie_measure_dir, program)
    return charlie_measure_dir, program

def check_directions(alice_measure_dir, bob_measure_dir, charlie_measure_dir):
    if alice_measure_dir == 'x' and bob_measure_dir == 'x':
        return charlie_measure_dir == 'x'
    if alice_measure_dir == 'x' and bob_measure_dir == 'y':
        return charlie_measure_dir == 'y'
    if alice_measure_dir == 'y' and bob_measure_dir == 'x':
        return charlie_measure_dir == 'y'
    if alice_measure_dir == 'y' and bob_measure_dir == 'y':
        return charlie_measure_dir == 'x'
    print("Should never get here")

def bob_and_charlie(bob_measure_result, charlie_measure_result):
    # at this point we know the directions are valid
    if charlie_measure_result == 1:
        return int(not bob_measure_result)
    else:
        return bob_measure_result

# from docs.rigetti.com
def ghz_state(qubits, program):
    program += H(qubits[0])
    for q1, q2 in zip(qubits, qubits[1:]):
        program += CNOT(q1, q2)
    return program

def initial_setup():
    message = random.getrandbits(MSG_LENGTH)
    
    alice_qubit = 0
    bob_qubit = 1
    charlie_qubit = 2
    
    program = Program()
    
    # entangle qubits (GHZ)
    program = ghz_state([alice_qubit, bob_qubit, charlie_qubit], program)

    return alice_qubit, bob_qubit, charlie_qubit, program



MSG_LENGTH = 1 
NUM_TRIALS = 100 
retries = 0
qc = get_qc("9q-square-qvm")
for trial in range(NUM_TRIALS):

    # perform secret sharing procedure once per message bit
    for i in range(MSG_LENGTH):
        while (True): # retry until success
            alice_q, bob_q, charlie_q, program = initial_setup()
            alice_measure_dir, program = alice(alice_q, program)
            bob_measure_dir, program = bob(bob_q, program)
            charlie_measure_dir, program = charlie(charlie_q, program)
            should_abort = not check_directions(alice_measure_dir, bob_measure_dir, charlie_measure_dir)
            if should_abort:
                print("Abort! Measurements yielded no useful information. Retrying...") 
                retries += 1
                continue
            # run program, now that we know results will be interesting
            #qvm = QVMConnection()
            program = qc.compiler.quil_to_native_quil(program)
            program = add_decoherence_noise(program)
            program = program.measure_all() 
            #results = qvm.run(program)[0]
            results = qc.run(program)[0]
            alice_measure_result = results[0]
            bob_measure_result = results[1]
            charlie_measure_result = results[2]
            
            joint_result = bob_and_charlie(bob_measure_result, charlie_measure_result)
            print("Alice measured in " + alice_measure_dir + " and got " + str(alice_measure_result))
            print("Bob measured in " + bob_measure_dir + " and got " + str(bob_measure_result))
            print("Charlie measured in " + charlie_measure_dir + " and got " + str(charlie_measure_result))
            print("Bob and Charlie guessed " + str(joint_result))
            
            if joint_result == alice_measure_result:
                print("Success! Bob and Charlie reconstructed one bit of the secret message.")
                break
            else:
                print("Failure! Bob and Charlie reconstructed an incorrect bit of the secret message.")
                exit() # end proram, we have a bug

    print("Bob and Charlie succeeded with " + str(retries) + " retries.")

    




