from src.formatter.formatter import formatter


def lesson_1():
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
    import matplotlib.pyplot as plt
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.algorithms.optimizers import COBYLA, L_BFGS_B
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap
    from qiskit.utils import algorithm_globals

    from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier, VQC
    from qiskit_machine_learning.algorithms.regressors import NeuralNetworkRegressor, VQR
    from qiskit_machine_learning.neural_networks import SamplerQNN, EstimatorQNN

    algorithm_globals.random_seed = 42

    formatter.clear_images()

    num_inputs = 2
    num_samples = 20
    X = 2 * algorithm_globals.random.random([num_samples, num_inputs]) - 1
    y01 = 1 * (np.sum(X, axis=1) >= 0)  # in { 0,  1}
    y = 2 * y01 - 1  # in {-1, +1}

    # construct QNN
    qc = QuantumCircuit(2)
    feature_map = ZZFeatureMap(2)
    ansatz = RealAmplitudes(2)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)

    estimator_qnn = EstimatorQNN(circuit=qc, input_params=feature_map.parameters, weight_params=ansatz.parameters)

    # QNN maps inputs to [-1, +1]
    estimator_qnn.forward(X[0, :], algorithm_globals.random.random(estimator_qnn.num_weights))

    # callback function that draws a live plot when the .fit() method is called
    def callback_graph(weights, obj_func_eval):
        objective_func_vals.append(obj_func_eval)

    # construct neural network classifier
    estimator_classifier = NeuralNetworkClassifier(estimator_qnn, optimizer=COBYLA(maxiter=60), callback=callback_graph)

    # create empty array for callback to store evaluations of the objective function
    objective_func_vals = []
    plt.rcParams["figure.figsize"] = (12, 6)

    # fit classifier to data
    estimator_classifier.fit(X, y)

    # return to default figsize
    plt.rcParams["figure.figsize"] = (6, 4)

    # score classifier
    estimator_classifier.score(X, y)

    # evaluate data points
    y_predict = estimator_classifier.predict(X)

    
    # red == wrongly classified
    for x, y_target, y_p in zip(X, y, y_predict):
        if y_target == 1:
            plt.plot(x[0], x[1], "bo")
        else:
            plt.plot(x[0], x[1], "go")
        if y_target != y_p:
            plt.scatter(x[0], x[1], s=200, facecolors="none", edgecolors="r", linewidths=2)
    
    plt.plot([-1, 1], [1, -1], "--", color="black")
    
    plt.show()
    
    # construct feature map
    feature_map = ZZFeatureMap(num_inputs)

    # construct ansatz
    ansatz = RealAmplitudes(num_inputs, reps=1)

    # construct quantum circuit
    qc = QuantumCircuit(num_inputs)
    qc.append(feature_map, range(num_inputs))
    qc.append(ansatz, range(num_inputs))
    savefile_path = formatter.file('construct_feature_map','png')
    qc.decompose().draw(output="mpl").savefig(savefile_path)