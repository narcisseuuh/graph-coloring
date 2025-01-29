# Import necessary libraries
from qiskit import QuantumCircuit

def grover(num_qubits):
    grover_circuit = QuantumCircuit(num_qubits)

    # Apply Hadamard gates to all qubits
    grover_circuit.h(range(num_qubits))

    # Oracle (example for a 3-qubit system, adjust as needed)
    grover_circuit.cz(0, 2)
    grover_circuit.cz(1, 2)

    # Diffusion operator
    grover_circuit.h(range(num_qubits))
    grover_circuit.x(range(num_qubits))
    grover_circuit.h(num_qubits - 1)
    grover_circuit.mct(list(range(num_qubits - 1)), num_qubits - 1)  # multi-controlled Toffoli
    grover_circuit.h(num_qubits - 1)
    grover_circuit.x(range(num_qubits))
    grover_circuit.h(range(num_qubits))

    return grover_circuit