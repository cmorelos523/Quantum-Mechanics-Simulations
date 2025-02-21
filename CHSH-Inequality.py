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
