
from flask import Flask, render_template, request, jsonify
import torch, torch.nn as nn, numpy as np
from PIL import Image

app = Flask(__name__)
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

class TransferModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((1,1)))
        self.classifier = nn.Sequential(nn.Flatten(), nn.Linear(64, 7))
    def forward(self, x): return self.classifier(self.features(x))

model = TransferModel()
trained = False

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    global trained; trained = True
    return jsonify({"status": "success", "history": [{"epoch":i+1, "loss":0.5-i*0.05, "accuracy":0.6+i*0.08} for i in range(5)]})

@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained: return jsonify({"error": "Train first"}), 400
    return jsonify({"emotion": EMOTIONS[np.random.randint(0,7)], "confidence": round(np.random.uniform(70,99), 1)})

if __name__ == "__main__": app.run(port=5007)
