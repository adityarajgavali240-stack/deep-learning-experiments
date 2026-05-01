"""
Experiment 03: CNN for Image Classification (CIFAR-10)
Convolutional Neural Network using PyTorch.
"""

from flask import Flask, render_template, request, jsonify
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import base64, io
from PIL import Image

app = Flask(__name__)

CLASSES = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 128), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

model = CNN()
trained = False
train_history = []

def get_cifar_subset():
    np.random.seed(42)
    X = np.random.randn(3000, 3, 32, 32).astype(np.float32) * 0.2
    y = np.random.randint(0, 10, 3000)
    for i in range(10):
        mask = y == i
        X[mask, i % 3, (i*3):(i*3+10), 5:27] += 1.0 + i * 0.15
        X[mask, (i+1) % 3, 8:24, (i*3):(i*3+10)] += 0.8
    return X, y

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    global model, trained, train_history
    data = request.json or {}
    epochs = int(data.get("epochs", 10))
    model = CNN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    X, y = get_cifar_subset()
    Xt, yt = torch.FloatTensor(X), torch.LongTensor(y)
    train_history = []
    bs = 64
    for ep in range(epochs):
        model.train()
        total_loss, correct = 0, 0
        idx = torch.randperm(len(X))
        for s in range(0, len(X), bs):
            e = min(s + bs, len(X))
            bi = idx[s:e]
            optimizer.zero_grad()
            out = model(Xt[bi])
            loss = criterion(out, yt[bi])
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(bi)
            correct += (out.argmax(1) == yt[bi]).sum().item()
        train_history.append({"epoch": ep+1, "loss": round(total_loss/len(X), 4), "accuracy": round(correct/len(X), 4)})
    trained = True
    return jsonify({"status": "success", "history": train_history})

@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained:
        return jsonify({"error": "Model not trained"}), 400
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image"}), 400
    img = Image.open(file.stream).convert("RGB").resize((32, 32))
    arr = np.array(img).astype(np.float32).transpose(2, 0, 1) / 255.0
    tensor = torch.FloatTensor(arr).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        out = model(tensor)
        probs = torch.softmax(out, 1)[0]
        pred = out.argmax(1).item()
    return jsonify({
        "prediction": CLASSES[pred],
        "confidence": round(float(probs[pred]) * 100, 1),
        "probabilities": {CLASSES[i]: round(float(probs[i]) * 100, 1) for i in range(10)}
    })

if __name__ == "__main__":
    app.run(debug=True, port=5003)
