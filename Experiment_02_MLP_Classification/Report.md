# Experiment 02 — Implementation of Multilayer Perceptron (MLP) for Classification

## Title
Implementation of Multilayer Perceptron (MLP) for Handwritten Digit Classification (MNIST)

## Aim
To build and train a Multilayer Perceptron (MLP) model using PyTorch for the classification of handwritten digits from the MNIST dataset.

## Objectives
- Understand the architecture of a Multilayer Perceptron.
- Implement MLP using PyTorch with Dense (Linear) layers.
- Train the model on the MNIST dataset.
- Evaluate classification accuracy and visualize training curves.
- Provide interactive digit drawing and real-time classification.

## Software Required
Python 3.x, Flask, PyTorch, NumPy, Pillow, Web Browser

## Theory
A Multilayer Perceptron (MLP) is a class of feedforward artificial neural network. An MLP consists of at least three layers: input, hidden, and output. Each node uses a nonlinear activation function. The MLP architecture used here has:
- **Input Layer:** 784 neurons (28×28 flattened image pixels)
- **Hidden Layer 1:** 256 neurons with ReLU activation and 20% Dropout
- **Hidden Layer 2:** 128 neurons with ReLU activation and 20% Dropout
- **Output Layer:** 10 neurons with Softmax for digit classes 0-9

Training uses Adam optimizer with Cross-Entropy loss.

## Procedure
1. Load and normalize the MNIST dataset.
2. Flatten 28×28 images into 784-dimensional vectors.
3. Define the MLP architecture with Linear, ReLU, and Dropout layers.
4. Compile with Adam optimizer and CrossEntropyLoss.
5. Train for the specified number of epochs.
6. Evaluate accuracy on test data.
7. Provide a canvas-based drawing interface for live digit classification.

## How to Run
```bash
pip install flask torch numpy pillow
python app.py
```
Open http://localhost:5002 in your browser.

## Conclusion
The MLP model successfully learned to classify handwritten digits from the MNIST dataset. The interactive web interface allows users to draw digits and see real-time classification with confidence probabilities, demonstrating the practical application of feedforward neural networks.
