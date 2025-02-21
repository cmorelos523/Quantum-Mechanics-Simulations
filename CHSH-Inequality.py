# import necessary modules
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
#from qiskit import execute
from qiskit.visualization import plot_histogram

# Measurement transformations:
# For qubit 0, measuring in the X basis is achieved by applying a Hadamard (H).
# For qubit 1, we transform into the basis of the observable.
def XW(circ, qbit0, qbit1):
    # Qubit 0: X measurement -> convert to Z via H
    circ.h(qbit0)
    # Qubit 1: W measurement -> convert to Z using S, H, T, H
    circ.s(qbit1)
    circ.h(qbit1)
    circ.t(qbit1)
    circ.h(qbit1)

def XV(circ, qbit0, qbit1):
    # Qubit 0: X measurement -> convert to Z
    circ.h(qbit0)
    # Qubit 1: V measurement -> convert to Z using S, H, T†, H
    circ.s(qbit1)
    circ.h(qbit1)
    circ.tdg(qbit1)
    circ.h(qbit1)

def ZW(circ, qbit0, qbit1):
    # Qubit 0: Z measurement is the default (do nothing)
    # Qubit 1: W measurement -> convert to Z using S, H, T, H
    circ.s(qbit1)
    circ.h(qbit1)
    circ.t(qbit1)
    circ.h(qbit1)

def ZV(circ, qbit0, qbit1):
    # Qubit 0: Z measurement (default)
    # Qubit 1: V measurement -> convert to Z using S, H, T†, H
    circ.s(qbit1)
    circ.h(qbit1)
    circ.tdg(qbit1)
    circ.h(qbit1)

# Function to create a cat state: |ψ⟩ = (|00⟩ + |11⟩)/√2
def create_cat():
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    return circ

# Helper function to compute the expectation value from measurement counts.
# For each 2-bit outcome, we assign +1 if the bit is 0 and -1 if 1.
# The product of the outcomes for qubits 0 and 1 is computed, so that:
# '00' or '11' → +1, and '01' or '10' → -1.
def expectation(counts, shots):
    # Using the fact that (counts['00']+counts['11'] - counts['01']-counts['10'])/shots is the expectation.
    exp_val = (counts.get('00', 0) + counts.get('11', 0) - counts.get('01', 0) - counts.get('10', 0))
    return exp_val / shots

# Set number of shots and create lists for circuits, labels, and functions
shots = 1024
circuits = []
labels = ["XW", "XV", "ZW", "ZV"]
transformation_functions = [XW, XV, ZW, ZV]

# Build the circuits for each measurement setting.
for func in transformation_functions:
    qc = create_cat()  # create the entangled state
    func(qc, 0, 1)     # apply the measurement transformation for the particular observable
    qc.measure_all()   # measure both qubits in the computational (Z) basis
    circuits.append(qc)

# Use the Qiskit Aer simulator.
backend = Aer.get_backend('qasm_simulator')

# Instead of using the deprecated execute() function,
# we transpile the circuits for the backend and then run them.
transpiled_circuits = transpile(circuits, backend)
job = backend.run(transpiled_circuits, shots=shots)
results = job.result()

# Extract counts and compute expectation values
expectations = []
for label, qc in zip(labels, circuits):
    counts = results.get_counts(qc)
    exp_val = expectation(counts, shots)
    expectations.append(exp_val)
    print(f"Expectation for {label}: {exp_val}")

# Compute the CHSH correlation parameter:
# C_quantum = ⟨XW⟩ - ⟨XV⟩ + ⟨ZW⟩ + ⟨ZV⟩
C_quantum = expectations[0] - expectations[1] + expectations[2] + expectations[3]
print("C_quantum =", C_quantum)
print("|C_quantum| =", abs(C_quantum))

# Plot histograms of measurement counts in a 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
for i, qc in enumerate(circuits):
    counts = results.get_counts(qc)
    ax = axs[i // 2, i % 2]
    plot_histogram(counts, ax=ax, title=labels[i])
plt.tight_layout()
plt.show()
