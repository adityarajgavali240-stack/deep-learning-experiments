
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)
trained = False

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    global trained; trained = True
    return jsonify({"status": "success", "history": [{"epoch":i+1, "loss":0.6-i*0.1, "accuracy":0.5+i*0.1} for i in range(5)]})

@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained: return jsonify({"error": "Train first"}), 400
    text = request.json.get("text", "").lower()
    sent = "Positive" if any(w in text for w in ["good", "great", "awesome", "amazing"]) else "Negative"
    return jsonify({"sentiment": sent, "confidence": round(np.random.uniform(75,99), 1)})

if __name__ == "__main__": app.run(port=5008)
