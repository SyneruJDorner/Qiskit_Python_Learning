import qiskit
import numpy as np
from qiskit import Aer, QuantumCircuit, execute, ClassicalRegister, QuantumRegister, BasicAer
from qiskit.visualization import plot_bloch_multivector
from qiskit.visualization import plot_histogram
from math import pi, sqrt

def execute():
    print(Aer.backends())
    print("Hello World!")