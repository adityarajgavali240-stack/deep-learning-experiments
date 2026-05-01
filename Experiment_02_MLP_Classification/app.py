"""
Experiment 02: Implementation of MLP for Classification (MNIST)
Multilayer Perceptron using PyTorch for handwritten digit recognition.
"""

from flask import Flask, render_template, request, jsonify
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import base64, io, json, os
from PIL import Image

app = Flask(__name__)

# ============ MLP MODEL ============

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.net(x)


model = MLP()
trained = False
train_history = []


def get_mnist_subset():
    """Generate synthetic MNIST-like data for demo training."""
    np.random.seed(42)
    X_train = np.random.randn(2000, 1, 28, 28).astype(np.float32) * 0.3
    y_train = np.random.randint(0, 10, 2000)
    # Create distinct patterns for each digit
    for i in range(10):
        mask = y_train == i
        X_train[mask, 0, i*2:i*2+8, 5:23] += 1.0 + i * 0.1
        X_train[mask, 0, 10:18, i*2:i*2+8] += 0.8 + i * 0.1
    return X_train, y_train


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/train", methods=["POST"])
def train():
    global model, trained, train_history
    data = request.json or {}
    epochs = int(data.get("epochs", 10))
    lr = float(data.get("lr", 0.001))

    model = MLP()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    X_train, y_train = get_mnist_subset()
    X_tensor = torch.FloatTensor(X_train)
    y_tensor = torch.LongTensor(y_train)

    train_history = []
    batch_size = 64
    n = len(X_train)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        correct = 0
        indices = torch.randperm(n)
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            idx = indices[start:end]
            xb = X_tensor[idx]
            yb = y_tensor[idx]

            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(xb)
            correct += (out.argmax(1) == yb).sum().item()

        avg_loss = total_loss / n
        accuracy = correct / n
        train_history.append({"epoch": epoch + 1, "loss": round(avg_loss, 4), "accuracy": round(accuracy, 4)})

    trained = True
    return jsonify({"status": "success", "history": train_history})


@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained:
        return jsonify({"error": "Model not trained yet"}), 400

    data = request.json
    pixels = data.get("pixels", [])

    if not pixels:
        return jsonify({"error": "No pixel data"}), 400

    img_array = np.array(pixels, dtype=np.float32).reshape(1, 1, 28, 28)
    tensor = torch.FloatTensor(img_array)

    model.eval()
    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)[0]
        pred = output.argmax(1).item()

    return jsonify({
        "prediction": pred,
        "confidence": round(float(probs[pred]) * 100, 1),
        "probabilities": [round(float(p) * 100, 1) for p in probs]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5002)
