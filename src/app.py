from src.formatter.formatter import formatter


def lesson_1():
    import numpy as np
    from qiskit import QuantumCircuit, transpile
    from qiskit.providers.aer import QasmSimulator
    from qiskit.visualization import plot_histogram
    formatter.clear_images()

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

    # Draw the circuit
    file_path = formatter.file("quantum_circuit_start", "png")
    circuit.draw(output="mpl", filename=file_path)

    # Plot a histogram
    file_path = formatter.file("quantum_histogram", "png")
    plot_histogram(counts).savefig(file_path)


def lesson_2():
    from qiskit.primitives import Sampler
    from qiskit_machine_learning.neural_networks import SamplerQNN
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_machine_learning.neural_networks import EstimatorQNN
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import RealAmplitudes
    from qiskit.utils import algorithm_globals

    formatter.clear_images()
    
    # set random seed for reproducibility
    algorithm_globals.random_seed = 42

    # construct parametrized circuit
    params1 = [Parameter("input1"), Parameter("weight1")]
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.ry(params1[0], 0)
    qc1.rx(params1[1], 0)
    savefile_path = formatter.file('qnn','png')
    qc1.draw("mpl").savefig(savefile_path)
    observable1 = SparsePauliOp.from_list([("Y" * qc1.num_qubits, 1)])
    qnn1 = EstimatorQNN(circuit=qc1, observables=observable1, input_params=[params1[0]], weight_params=[params1[1]])
    
    # define (random) input and weights
    input1 = algorithm_globals.random.random(qnn1.num_inputs)
    weights1 = algorithm_globals.random.random(qnn1.num_weights)

    # QNN forward pass
    test= qnn1.forward(input1, weights1)
    print(test)

    # QNN batched forward pass
    test2 = qnn1.forward([input1, input1], weights1)
    print(test2)

    # QNN backward pass
    test3 = qnn1.backward(input1, weights1)
    print(test3)
    # QNN batched backward pass
    test4 = qnn1.backward([input1, input1], weights1)
    print(test4)

    observable2 = SparsePauliOp.from_list([("Z" * qc1.num_qubits, 1)])
    qnn2 = EstimatorQNN(
        circuit=qc1,
        observables=[observable1, observable2],
        input_params=[params1[0]],
        weight_params=[params1[1]],
    )

    # QNN forward pass
    test5 = qnn2.forward(input1, weights1)
    print(test5)
    # QNN backward pass
    test6 = qnn2.backward(input1, weights1)
    print(test6)

    qc = RealAmplitudes(2, entanglement="linear", reps=1)
    savefile_path = formatter.file('realAmplitudes','png')
    qc.draw(output="mpl").savefig(savefile_path)

    # specify sampler-based QNN
    qnn4 = SamplerQNN(circuit=qc, input_params=[], weight_params=qc.parameters)

    # define (random) input and weights
    input4 = algorithm_globals.random.random(qnn4.num_inputs)
    weights4 = algorithm_globals.random.random(qnn4.num_weights)

    # QNN forward pass
    test7 = qnn4.forward(input4, weights4)
    print(test7)
    
    # QNN backward pass, returns a tuple of matrices, None for the gradients with respect to input data.
    test8 = qnn4.backward(input4, weights4)
    print(test8)


def execute_app():
    print("Hello World!")
    pass