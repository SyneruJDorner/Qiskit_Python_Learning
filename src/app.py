import os, time, qiskit
import numpy as np
from qiskit import Aer, QuantumCircuit, execute, ClassicalRegister, QuantumRegister, BasicAer
from qiskit.visualization import plot_bloch_multivector
from qiskit.visualization import plot_histogram
from math import pi, sqrt

from .config import config


def clear_previous_images():
    for file in os.listdir(config.IMAGES_PATH):
        os.remove(os.path.join(config.IMAGES_PATH, file))


def get_formated_name(file_name):
    date_time_formated = time.strftime("%Y_%m_%d_%H_%M_%S")
    file_format = "png"
    formated_name = f"{file_name}_{date_time_formated}.{file_format}"
    
    #Check if file exists and if it does, add a number to the end of the file name each time in a while loop
    number = 0
    while True:
        if os.path.exists(os.path.join(config.IMAGES_PATH, formated_name)):
            number += 1
            formated_name = f"{file_name}_{date_time_formated}_{number}.{file_format}"
        else:
            break
    
    return os.path.join(config.IMAGES_PATH, formated_name)


def print_circuit_test():
    cr = ClassicalRegister(1, "cr")
    qr = QuantumRegister(1, "qr")
    qc = QuantumCircuit(qr, cr)

    file_path = get_formated_name("quantum_circuit")
    qc.draw(output="mpl", filename=file_path)


def print_qubit_orientation(orientation: float):
    if orientation == 0:
        qr = QuantumRegister(1, "qr")
        qc = QuantumCircuit(qr)
        file_path = get_formated_name("quantum_circuit_start")
        qc.draw(output="mpl", filename=file_path)
        backend = Aer.get_backend("statevector_simulator")
        result = execute(qc, backend).result().get_statevector(qc, decimals=3)
        file_path = get_formated_name("quantum_multivector_start")
        plot_bloch_multivector(result).savefig(file_path)

    if orientation == 1:
        qr_x = QuantumRegister(1, "qr")
        qc_x = QuantumCircuit(qr_x)
        qc_x.x(qr_x[0])
        file_path = get_formated_name("quantum_circuit_after_x_gate")
        qc_x.draw(output="mpl", filename=file_path)
        backend = Aer.get_backend("statevector_simulator")
        result = execute(qc_x, backend).result().get_statevector(qc_x, decimals=3)
        file_path = get_formated_name("quantum_multivector_after_x_gate")
        plot_bloch_multivector(result).savefig(file_path)


def print_measure_classical_register():
    cr_x = ClassicalRegister(1, "cr")
    qr_x = QuantumRegister(1, "qr")
    qc_x = QuantumCircuit(qr_x, cr_x)
    qc_x.x(qr_x[0])
    qc_x.measure(qr_x, cr_x)
    file_path = get_formated_name("quantum_circuit_measure")
    qc_x.draw(output="mpl", filename=file_path)


def print_measure_classical_register_x_times(x):
    cr_x = ClassicalRegister(1, "cr")
    qr_x = QuantumRegister(1, "qr")
    qc_x = QuantumCircuit(qr_x, cr_x)
    qc_x.x(qr_x[0])

    backend = BasicAer.get_backend("qasm_simulator")
    job = execute(qc_x, backend, shots=x)
    result = job.result()
    count = result.get_counts(qc_x)
    file_path = get_formated_name("quantum_histogram")
    plot_histogram(count).savefig(file_path)


def print_quantum_circuit_2_qubits():
    cr = ClassicalRegister(3, "cr")
    qr = QuantumRegister(3, "qr")
    qc = QuantumCircuit(qr, cr)
    qc.x(0)
    qc.barrier()
    qc.measure([0, 1], [0, 1])
    file_path = get_formated_name("quantum_circuit_2_qubits")
    qc.draw(output="mpl", filename=file_path)


def print_quantum_circuit_all_qubits():
    qr = QuantumRegister(5, "qr")
    qc = QuantumCircuit(qr, name="qc")
    qc.x(0)
    qc.measure_all()
    file_path = get_formated_name("quantum_circuit_2_qubits")
    qc.draw(output="mpl", filename=file_path)


def execute_app():
    clear_previous_images()

    print(Aer.backends())       # Aer library is writen in C++
    print(BasicAer.backends())  # BasicAer library is writen in python

    #print_circuit_test()
    print_qubit_orientation(0)
    print_qubit_orientation(1)
    print_measure_classical_register()
    print_measure_classical_register_x_times(1000)
    print_quantum_circuit_2_qubits()
    print_quantum_circuit_all_qubits()
