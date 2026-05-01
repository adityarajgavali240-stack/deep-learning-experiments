"""
Experiment 04: CNN for Facial Emotion Detection
Custom CNN for 7-class emotion classification from face images.
"""

from flask import Flask, render_template, request, jsonify
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from PIL import Image

app = Flask(__name__)
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

class EmotionCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Dropout2d(0.25),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Dropout2d(0.25),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(128 * 6 * 6, 512), nn.ReLU(), nn.Dropout(0.5), nn.Linear(512, 7)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

model = EmotionCNN()
trained = False
history = []

def gen_data():
    np.random.seed(42)
    X = np.random.randn(2100, 1, 48, 48).astype(np.float32) * 0.3
    y = np.random.randint(0, 7, 2100)
    for i in range(7):
        m = y == i
        X[m, 0, i*5:i*5+15, 10:38] += 0.8 + i * 0.12
    return X, y

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    global model, trained, history
    epochs = int((request.json or {}).get("epochs", 10))
    model = EmotionCNN()
    opt = optim.Adam(model.parameters(), lr=0.001)
    crit = nn.CrossEntropyLoss()
    X, y = gen_data()
    Xt, yt = torch.FloatTensor(X), torch.LongTensor(y)
    history = []
    for ep in range(epochs):
        model.train(); tl = tc = 0; idx = torch.randperm(len(X))
        for s in range(0, len(X), 64):
            e = min(s+64, len(X)); bi = idx[s:e]
            opt.zero_grad(); out = model(Xt[bi]); loss = crit(out, yt[bi])
            loss.backward(); opt.step()
            tl += loss.item()*len(bi); tc += (out.argmax(1)==yt[bi]).sum().item()
        history.append({"epoch": ep+1, "loss": round(tl/len(X),4), "accuracy": round(tc/len(X),4)})
    trained = True
    return jsonify({"status": "success", "history": history})

@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained:
        return jsonify({"error": "Train first"}), 400
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image"}), 400
    img = Image.open(file.stream).convert("L").resize((48, 48))
    arr = np.array(img).astype(np.float32).reshape(1, 1, 48, 48) / 255.0
    model.eval()
    with torch.no_grad():
        out = model(torch.FloatTensor(arr))
        probs = torch.softmax(out, 1)[0]
        pred = out.argmax(1).item()
    return jsonify({
        "emotion": EMOTIONS[pred],
        "confidence": round(float(probs[pred])*100, 1),
        "all_emotions": {EMOTIONS[i]: round(float(probs[i])*100,1) for i in range(7)}
    })

if __name__ == "__main__":
    app.run(debug=True, port=5004)
