import os, time
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





def execute_app():
    import numpy as np
    from qiskit import QuantumCircuit, transpile
    from qiskit.providers.aer import QasmSimulator
    from qiskit.visualization import plot_histogram
    clear_previous_images()

    # Use Aer's qasm_simulator
    simulator = QasmSimulator()

    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(2, 2)

    # Add a H gate on qubit 0
    circuit.h(0)

    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)

    # Map the quantum measurement to the classical bits
    circuit.measure([0,1], [0,1])

    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    compiled_circuit = transpile(circuit, simulator)

    # Execute the circuit on the qasm simulator
    job = simulator.run(compiled_circuit, run=1000)

    # Grab results from the job
    result = job.result()

    # Returns counts
    counts = result.get_counts(compiled_circuit)
    print("\nTotal count for 00 and 11 are:",counts)

    # Draw the circuit
    file_path = get_formated_name("quantum_circuit_start")
    circuit.draw(output="mpl", filename=file_path)

    # Plot a histogram
    file_path = get_formated_name("quantum_histogram")
    plot_histogram(counts).savefig(file_path)

    