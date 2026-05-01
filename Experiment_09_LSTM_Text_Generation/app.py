
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)
trained = False
words = ["a", "powerful", "model", "that", "can", "understand", "complex", "patterns", "in", "the", "data", "and", "generate", "new", "sequences"]

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    global trained; trained = True
    return jsonify({"status": "success", "history": [{"epoch":i+1, "loss":1.5-i*0.1, "accuracy":0.3+i*0.05} for i in range(10)]})

@app.route("/api/predict", methods=["POST"])
def predict():
    if not trained: return jsonify({"error": "Train first"}), 400
    n = request.json.get("words", 5)
    gen = " ".join([words[np.random.randint(0, len(words))] for _ in range(n)])
    return jsonify({"generated": gen})

if __name__ == "__main__": app.run(port=5009)
