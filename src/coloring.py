import numpy as np
from graph import QuantumGraph
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer.noise import NoiseModel
from matplotlib import pyplot as plt
from IPython.display import display
from w_state import F_gate, cxrv
from grover import grover

def color(g : QuantumGraph, k = 3) -> np.matrix:
    """
    Quantum algorithm for graph k-coloring.

    Parameters:
        g: A graph which we want to color,
        k: int, number of colors to use in the coloring.

    Returns:
        colors: np.matrix, representing the graph coloring (binary matrix).
    """
    adjacency = g.adjacency_matrix()
    n_nodes = len(g.nodes())
    colors = np.zeros((n_nodes, k))
    nb_qubits = n_nodes * k 

    qreg = QuantumRegister(nb_qubits + len(g.edges()) + 1, "q")
    # auxiliary qubits added for each arc of the graph
    creg = ClassicalRegister(nb_qubits, "c")
    circuit = QuantumCircuit(qreg, creg)

    # Step 1: Initialize the superposition of all possible colorings
    # ========================================================
    # this part was designed only for the case k = 3 so far...
    # ========================================================
    for i in range(0, nb_qubits, k):
        circuit.x(qreg[i + 2]) #start is |100>
        F_gate(circuit,qreg,i + 2,i + 1,i + 3,i + 1) # Applying F12
        F_gate(circuit,qreg,i + 1,i,i + 3,i + 2) # Applying F23

        circuit.cx(qreg[i + 1],qreg[i + 2]) # cNOT 21
        circuit.cx(qreg[i],qreg[i + 1]) # cNOT 32

    circuit.barrier()

    # Step 2: Apply constraints to ensure valid colorings
    auxiliary = nb_qubits
    for (node1, node2) in g.edges():
        for j in range(k):
            circuit.ccx(qreg[node1 * k + j], qreg[node2 * k + j], qreg[auxiliary])
        auxiliary += 1

    circuit.barrier()

    # Step 3: Apply CX extended gate from each auxiliary qubit to the last
    last_auxiliary = auxiliary
    for i in range(nb_qubits, auxiliary):
        circuit.x(i)
        circuit.cx(qreg[i], qreg[last_auxiliary])

    circuit.barrier()

    # Step 5: Measurement
    for i in range(nb_qubits):
        circuit.measure(qreg[i], creg[i])

    # Simulate the circuit
    simulator = AerSimulator()
    circuit = circuit.decompose()  # Decompose custom gates into standard gates
    result = simulator.run(circuit, shots=4000).result()
    counts = result.get_counts()

    most_probable = max(counts, key=counts.get)
    binary_result = [int(bit) for bit in most_probable[::-1]]

    # Convert the result into the coloring matrix
    for i in range(n_nodes):
        for j in range(k):
            colors[i][j] = binary_result[i * k + j]

    return np.matrix(colors)

if __name__ == '__main__':
    n = 4
    k = 3

    G = QuantumGraph.gen_random(n)

    color_matrix = color(G, k)
    print(color_matrix)

    G.show_coloring(color_matrix)
