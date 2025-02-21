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
