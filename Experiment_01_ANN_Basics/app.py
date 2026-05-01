"""
Experiment 01: Implementation of Artificial Neural Network (ANN) Basics
ANN from scratch using NumPy to solve the XOR problem.
"""

from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# ============ ANN FROM SCRATCH ============

class ANN:
    def __init__(self, layer_sizes, lr=0.5):
        self.lr = lr
        self.weights = []
        self.biases = []
        self.history = []
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.5
            b = np.zeros((1, layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_deriv(self, x):
        return x * (1.0 - x)

    def forward(self, X):
        self.activations = [X]
        current = X
        for w, b in zip(self.weights, self.biases):
            z = np.dot(current, w) + b
            current = self.sigmoid(z)
            self.activations.append(current)
        return current

    def backward(self, y):
        m = y.shape[0]
        deltas = [None] * len(self.weights)
        error = y - self.activations[-1]
        deltas[-1] = error * self.sigmoid_deriv(self.activations[-1])
        for i in range(len(self.weights) - 2, -1, -1):
            error = deltas[i + 1].dot(self.weights[i + 1].T)
            deltas[i] = error * self.sigmoid_deriv(self.activations[i + 1])
        for i in range(len(self.weights)):
            self.weights[i] += self.activations[i].T.dot(deltas[i]) * self.lr / m
            self.biases[i] += np.sum(deltas[i], axis=0, keepdims=True) * self.lr / m

    def train(self, X, y, epochs=5000):
        self.history = []
        for epoch in range(epochs):
            output = self.forward(X)
            loss = np.mean((y - output) ** 2)
            self.backward(y)
            if epoch % 100 == 0:
                self.history.append({"epoch": epoch, "loss": round(float(loss), 6)})
        output = self.forward(X)
        loss = np.mean((y - output) ** 2)
        self.history.append({"epoch": epochs, "loss": round(float(loss), 6)})
        return self.history

    def predict(self, X):
        return self.forward(X)


# XOR Data
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([[0], [1], [1], [0]])

model = ANN([2, 4, 1], lr=2.0)
training_done = False
train_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/train", methods=["POST"])
def train():
    global model, training_done, train_history
    data = request.json or {}
    epochs = int(data.get("epochs", 5000))
    lr = float(data.get("lr", 2.0))
    model = ANN([2, 4, 1], lr=lr)
    train_history = model.train(X_xor, y_xor, epochs=epochs)
    training_done = True

    predictions = model.predict(X_xor).flatten().tolist()
    results = []
    for i in range(4):
        results.append({
            "input": X_xor[i].tolist(),
            "expected": int(y_xor[i][0]),
            "predicted": round(predictions[i], 4),
            "rounded": int(round(predictions[i]))
        })

    return jsonify({
        "status": "success",
        "history": train_history,
        "results": results,
        "weights": [w.tolist() for w in model.weights],
        "biases": [b.tolist() for b in model.biases]
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    if not training_done:
        return jsonify({"error": "Model not trained yet. Train first."}), 400
    data = request.json
    x1 = float(data.get("x1", 0))
    x2 = float(data.get("x2", 0))
    inp = np.array([[x1, x2]])
    out = model.predict(inp)[0][0]
    return jsonify({
        "input": [x1, x2],
        "output": round(float(out), 6),
        "classification": int(round(float(out)))
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
