# Experiment 01 — Implementation of Artificial Neural Network (ANN) Basics

## Title
Implementation of Artificial Neural Network (ANN) from Scratch to Solve the XOR Problem

## Aim
To understand and implement a basic Artificial Neural Network (ANN) from scratch using NumPy, demonstrating the forward pass, backpropagation, and gradient descent optimization on the non-linearly separable XOR problem.

## Objectives
- Understand the structure and working of a feedforward neural network.
- Implement activation functions (Sigmoid) and their derivatives.
- Implement the forward propagation algorithm.
- Implement the backpropagation algorithm for weight updates.
- Train the ANN to solve the XOR logical operation.
- Visualize the training loss convergence.

## Software Required
Python 3.x, Flask, NumPy, Web Browser

## Theory
An Artificial Neural Network (ANN) is a computational model inspired by the biological neural networks in the human brain. It consists of interconnected nodes (neurons) organized in layers — an input layer, one or more hidden layers, and an output layer.

The XOR problem is a classic non-linearly separable problem that cannot be solved by a single-layer perceptron. It requires at least one hidden layer to learn the non-linear decision boundary.

### Key Concepts:
- **Forward Propagation:** Input signals are passed through the network layer by layer. Each neuron computes a weighted sum of its inputs, adds a bias, and applies an activation function.
- **Sigmoid Activation:** σ(x) = 1 / (1 + e^(-x)), maps values to range (0, 1).
- **Backpropagation:** The error at the output is propagated backward through the network to compute gradients of the loss with respect to each weight.
- **Gradient Descent:** Weights are updated in the direction that minimizes the loss: w = w - lr * ∂L/∂w.

### Network Architecture:
- Input Layer: 2 neurons (X1, X2)
- Hidden Layer: 4 neurons with Sigmoid activation
- Output Layer: 1 neuron with Sigmoid activation

## Procedure
1. Import NumPy and Flask libraries.
2. Define the Sigmoid activation function and its derivative.
3. Initialize random weights and biases for all layers.
4. Implement forward propagation to compute output.
5. Calculate Mean Squared Error (MSE) loss.
6. Implement backpropagation to compute gradients.
7. Update weights and biases using gradient descent.
8. Repeat steps 4-7 for the specified number of epochs.
9. Evaluate the trained model on all XOR inputs.
10. Serve a web interface for interactive training and prediction.

## How to Run
```bash
pip install flask numpy
python app.py
```
Open http://localhost:5001 in your browser.

## Conclusion
The experiment successfully demonstrated the implementation of an ANN from scratch using NumPy. The network learned to solve the XOR problem through backpropagation, achieving correct classification for all four input combinations. This experiment reinforced understanding of neural network fundamentals including forward propagation, backpropagation, and gradient descent optimization.
